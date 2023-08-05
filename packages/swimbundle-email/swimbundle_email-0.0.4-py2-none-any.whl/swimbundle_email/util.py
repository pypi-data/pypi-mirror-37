import re
import quopri
import hashlib
import magic
import base64
import pendulum
import pendulum.parsing.exceptions


class EmailParser(object):
    def __init__(self, filename, email_data):
        self.filename = filename
        self.email_data = email_data

    def get_reply_to(self):
        raise NotImplementedError

    def get_sender(self):
        raise NotImplementedError

    def get_plaintext_body(self):
        raise NotImplementedError

    def get_html_body(self, decode_html=True):
        raise NotImplementedError

    def get_rtf_body(self):
        raise NotImplementedError

    def get_subject(self):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_recipients(self):
        raise NotImplementedError

    def get_headers(self):
        raise NotImplementedError

    def get_attachments(self):
        raise NotImplementedError

    def get_id(self):
        raise NotImplementedError

    def get_date(self):
        raise NotImplementedError

    @staticmethod
    def _parse_regex(regex, *bodies):
        text = ""
        for body in bodies:
            text = text + body if body else text
        val = list(set(re.findall(regex, text)))
        return val

    def _get_authenticated_sender(self, headers):
        return ",".join(
            self._parse_regex('(?:Authenticated sender:) ([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', headers))

    def _get_clean_emails(self, email_data):
        valid_email_regex = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
        return ",".join(self._parse_regex(valid_email_regex, email_data))

    def _try_date_format(self, date_data):
        try:
            dt = pendulum.parse(date_data)
            return dt.to_iso8601_string()
        except pendulum.parsing.exceptions.ParserError:
            return date_data

    def parse(self, exclude_attachment_extensions=None):
        result = {
            "result": u"failure", "attachments_sha1": "", "attachments_md5": "",
            "attach_info": "", "headers": "",
            "recipients": "", "subject": "", "text_body": "", "html_body": "", "type": "", "attachments_sha256": ""
        }

        attachments = self.get_attachments()
        attachments_data = attachments.pop("attachments")  # Remove until we clean results
        if exclude_attachment_extensions:
            exclude_attachment_extensions = tuple(map(unicode.lower, exclude_attachment_extensions))
            attachments_data = filter(
                lambda attachment: not bool(unicode(attachment["filename"]).lower().endswith(exclude_attachment_extensions)),
                attachments_data
            )

        result.update(attachments)

        result["headers"] = ''.join(h[0] + ": " + h[1] + "\n" for h in self.get_headers())

        sender = self.get_sender()
        result["sender"] = sender if self._get_clean_emails(sender) else self._get_authenticated_sender(
            result['headers'])
        result["valid_sender_email"] = self._get_clean_emails(sender) or self._get_authenticated_sender(
            result['headers'])

        reply_to = self.get_reply_to()
        result["reply_to"] = reply_to
        result["valid_reply_to_email"] = self._get_clean_emails(reply_to)

        result["recipients"] = self.get_recipients()
        result["valid_recipients_email"] = self._get_clean_emails(self.get_recipients())

        result["subject"] = self.get_subject()
        result["text_body"] = self.get_plaintext_body()
        result["html_body"] = self.get_html_body()

        result["rtf_body"] = self.get_rtf_body()
        result["type"] = self.get_type()

        result["date"] = self._try_date_format(self.get_date())

        result["id"] = self.get_id()

        # Convert key, values to unicode (cleaning)
        content_charset = EmailUtil.check_content_charset(self)
        for k, v in result.iteritems():
            result[k] = v if v else ""
            if not isinstance(result[k], unicode):
                result[k] = result.pop(k).decode(content_charset, errors="replace")

        result["result"] = u"success"
        result["attachments"] = attachments_data  # Add back after cleaning
        return result


class EmailAttachmentList(object):
    """Container class for attachments, to standardize the output"""

    def __init__(self):
        self.attachments = []

    def add_attachment(self, email_attachment):
        if isinstance(email_attachment, EmailAttachment):
            self.attachments.append(email_attachment)
        else:
            raise Exception("Attempted to add attachment to EmailAttachments, invalid type detected")

    def to_swimlane_output(self):
        result = {
            "attach_info": [],
            "attachments": [],
            "attachments_md5": [],
            "attachments_sha1": [],
            "attachments_sha256": []
        }

        # Add all attachments into a list
        for attachment in self.attachments:
            result["attachments"].append(attachment.attachment_data)
            result["attach_info"].append(attachment.header_info)
            result["attachments_sha1"].append(attachment.hash_sha1)
            result["attachments_md5"].append(attachment.hash_md5)
            result["attachments_sha256"].append(attachment.hash_sha256)

        # Flatten results
        for k, v in result.iteritems():
            if k != "attachments":  # Don't flatten the attachments
                result[k] = ",".join(result[k])

        return result


class EmailAttachment(object):
    """Singular Attachment"""

    def __init__(self, header_info, filename, raw_data):
        """
        Create a singular email attachment object
        :param header_info: String of header information about the email
        :param filename: Filename of the attachment
        :param raw_data: Byte-like data, will be base64encoded
        """
        self.header_info = header_info
        self.raw_data = raw_data

        self.hash_md5 = hashlib.md5(raw_data).hexdigest()
        self.hash_sha1 = hashlib.sha1(raw_data).hexdigest()
        self.hash_sha256 = hashlib.sha256(raw_data).hexdigest()
        self.attachment_data = {
            "filename": filename,
            "base64": base64.b64encode(raw_data)
        }


class EmailUtil(object):

    # Check if the email base64 object conforms to rfc822
    @staticmethod
    def check_if_rfc_822(b64):
        file_decoded = base64.b64decode(b64)
        mime_type = magic.from_buffer(file_decoded, mime=True)
        if mime_type == "message/rfc822":
            return True
        else:
            return False

    # Tries to decode a mime encoded-word syntax string
    # See https://dmorgan.info/posts/encoded-word-syntax/ for more info
    @staticmethod
    def try_decode(text):
        if not text:
            return "(None)"

        result = u""

        for item in re.split(r'[\n\s]+', text):
            item = item.strip()
            match = re.match(r'=\?(.+)\?([B|Q])\?(.+)\?=', item)
            if match:
                charset, encoding, encoded_text = match.groups()
                if encoding is 'B':
                    byte_str = base64.b64decode(encoded_text)
                elif encoding is 'Q':
                    byte_str = quopri.decodestring(encoded_text)
                else:
                    # Can't decode this string, invalid encoding type
                    return text
                result = result + byte_str.decode(charset, errors="ignore")
            else:
                result = result + " " + item

        return result.strip() or text  # Return result if it's been populated, else original text

    @staticmethod
    def check_content_charset(parser):
        regex = r'(?:charset=\"?)([\w-]*)(?:\"+)'
        html_body = parser.get_html_body()
        headers = parser.get_headers()
        if headers:
            try:  # Try to get content charset from headers
                for header in headers:
                    if header[0].lower() == "content-type":
                        return re.findall(regex, " ".join(header))[0]
            except IndexError:
                pass
        if html_body:
            try:  # Try to get content charset from html_body
                return re.findall(regex, html_body)[0]
            except IndexError:
                pass
        return "utf-8"  # Default to utf-8 if we can't find it
