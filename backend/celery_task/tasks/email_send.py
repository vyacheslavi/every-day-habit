from backend.celery_task import celery_app
from backend.app.core.helpers import email_sender


@celery_app.task
def send_verification_email(
    receiver_email: str,
    token: str,
):
    email_sender.send_request_on_verify(
        receiver_email=receiver_email,
        token=token,
    )


@celery_app.task
def send_reset_password_email(
    receiver_email: str,
    token: str,
):
    email_sender.send_reset_password_email(
        receiver_email=receiver_email,
        token=token,
    )
