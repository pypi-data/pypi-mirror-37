"""
This module hold all the classes for the different email notification services like sendgrid, etc
"""
from django.core.mail import EmailMultiAlternatives
from herald.base import EmailNotification

class SendgridEmailNotification(EmailNotification):
    """
    This is to be used along with "django-sendgrid-v5" You must set
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    in your project
    """

    template_id = None


    def get_extra_data(self):
        """
        Returns a dictionary of extra data to be stored, and used for sending.
        MUST BE JSON SERIALIZABLE
        """

        return {
            'template_id': self.template_id,
            'substitutions': self.substitutions
        }

    @staticmethod
    # pylint: disable-msg=C0301,R0913
    def _send(recipients, text_content=None, html_content=None, sent_from=None, subject=None, extra_data=None,
              attachments=None):

        extra_data = extra_data or {}

        mail = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=sent_from,
            to=recipients,
            bcc=extra_data.get('bcc', None),
            headers=extra_data.get('headers', None),
            cc=extra_data.get('cc', None),
            reply_to=extra_data.get('reply_to', None),
        )

        if self.template_id:
            mail.template_id = self.template_id

        if html_content:
            mail.attach_alternative(html_content, 'text/html')

        for attachment in (attachments or []):
            # All mimebase attachments must have a Content-ID or Content-Disposition header
            # or they will show up as unnamed attachments"
            if isinstance(attachment, MIMEBase):
                if attachment.get('Content-ID', False):
                    # if you are sending attachment with content id,
                    # subtype must be 'related'.
                    mail.mixed_subtype = 'related'

                mail.attach(attachment)
            else:
                mail.attach(*attachment)

        mail.send()

