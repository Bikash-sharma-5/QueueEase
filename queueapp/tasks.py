from celery import shared_task
from django.core.mail import send_mail

@shared_task
def notify_users(email, queue_name, position):
    subject = "Your Queue Position is Near!"
    message = f"Hello, your position in the queue '{queue_name}' is now {position}. Please be prepared."
    send_mail(subject, message, 'noreply@queueease.com', [email])
    return f"Email sent to {email}"
