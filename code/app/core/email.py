from app.core.config import settings
import requests
from app.schemas.token import TokenEmail
from mailjet_rest import Client


class Email:
    def __init__(self, to, text):
        self.api_key = settings.MAILJET_API_KEY
        self.api_secret = settings.MAILJET_API_SECRET
        self.from_email = settings.MAILJET_FROM_EMAIL
        self.to: str = to  # email to send
        self.text: str = text
        self.subject: str = "Code validation"

    def send(self) -> TokenEmail:
        mailjet = Client(auth=(self.api_key, self.api_secret), version="v3.1")
        data = {
            "Messages": [
                {
                    "From": {"Email": self.from_email},
                    "To": [
                        {
                            "Email": self.to,
                        }
                    ],
                    "Subject": self.subject,
                    "TextPart": "Je sais pas",
                    "HTMLPart": self.text,
                    "CustomID": "Dailymotion",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result.status_code != 200:
            raise Exception("Error while sending email")
        # Create a TokenEmail object from the response
        return TokenEmail(
            from_email=self.from_email, to=self.to, subject=self.subject, text=self.text
        )
