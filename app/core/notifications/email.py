import mimetypes

from flask import render_template
from flask_mailman import EmailMessage


class BaseEmailNotification:

    def __init__(
        self,
        subject: str,
        destination: str,
        template: str,
        template_data: dict,
        cc: list[str] = [],
    ):
        self.subject = subject
        self.destination = destination
        self.template = template
        self.template_data = template_data
        self.cc = cc
        self.body = self._render_body()

    def _render_body(self) -> str:
        return render_template(self.template, **self.template_data)

    def _create_email(self) -> EmailMessage:
        email = EmailMessage(
            subject=self.subject, body=self.body, to=[self.destination], cc=self.cc
        )
        email.content_subtype = "html"
        return email

    def send(self) -> str:
        email = self._create_email()
        email.send()
        return f"Email with subject '{self.subject}' sent to {self.destination}"


class EmailNotification(BaseEmailNotification):
    pass


class AttachmentEmailNotification(BaseEmailNotification):

    def __init__(
        self,
        subject: str,
        destination: str,
        template: str,
        template_data: dict,
        attachment_file_paths: list[str],
        cc: list[str] = [],
    ):
        super().__init__(subject, destination, template, template_data, cc)
        self.attachment_file_paths = attachment_file_paths

    def send(self) -> str:
        email = self._create_email()

        for attachment_file_path in self.attachment_file_paths:
            with open(attachment_file_path, "rb") as f:
                filename = attachment_file_path.split("/")[-1]
                mime_type, _ = mimetypes.guess_type(attachment_file_path)
                if not mime_type:
                    mime_type = "application/octet-stream"
                email.attach(filename, f.read(), mime_type)

        email.send()
        return f"Email with subject '{self.subject}' and attachment sent to {self.destination}"
