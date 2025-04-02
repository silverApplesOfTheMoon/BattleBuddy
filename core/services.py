# Import Django's built-in send_mail function for sending emails
from django.core.mail import send_mail

"""
This file defines utility functions used throughout the Vets2Tech web application.
Specifically, it provides an email-sending helper function to centralize email logic.
"""

# Email Sending Utility

# Utility function to send an email
def send_email(email, subject, message):
    send_mail(
        subject,  # Subject of the email
        message,  # Message body of the email
        "secureprog123@gmail.com",  # Sender email
        [email],  # List of recipient email addresses
        fail_silently=False,  # Do not ignore errors during email sending
    )
