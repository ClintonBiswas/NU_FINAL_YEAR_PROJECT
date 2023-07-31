from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def send_staff_account_approval_email(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        subject = 'Staff Account Approval'
        message = 'Your request for a staff account has been approved.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.email]  # Make sure to pass the recipient email as a list or tuple

        # Send the email using the send_mail() function
        send_mail(subject, message, from_email, to_email, fail_silently=True)
