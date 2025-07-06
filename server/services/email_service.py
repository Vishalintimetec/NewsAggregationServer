from server.utils.email_utils import send_email

class EmailService:
    def send_notification_email(self, to_email: str, message: str):
        subject = "Your Notification Digest"
        body = f"Hello,\n\nYou have new notifications:\n\n{message}"
        send_email(to_email, subject, body)
