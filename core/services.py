from django.core.mail import send_mail

# Utility function to send an email
def send_email(email, subject, message):
    send_mail(
        subject,
        message,
        "secureprog123@gmail.com",
        [email],
        fail_silently=False,
    )
