from app.core.config import settings
from app.core.email import Email
import logging

LOGGER = logging.getLogger(__name__)


def test_mailgun_api_key_set():
    assert settings.MAILJET_API_KEY is not None


def test_send_email():
    # Instantiate the Email class
    email = Email(to="yitaf71708@chimpad.com", text="This is the text of the email")
    email.send()
