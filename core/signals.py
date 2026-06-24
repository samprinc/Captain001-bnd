from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from .services.email_service import EmailService

@receiver(post_save, sender=Booking)
def handle_booking_emails(sender, instance, created, **kwargs):
    """
    Acts as a traffic controller. When a booking is saved, it hands the 
    heavy lifting off to the background EmailService so the web server doesn't freeze.
    """
    
    # ------------------------------------------------------------------
    # CASE A: New Booking Created (Instant Confirmation)
    # ------------------------------------------------------------------
    if created:
        subject = f"We've received your brief: {instance.service_requested}"
        
        # 1. Fire the confirmation to the client in the background
        EmailService.send_client_async(
            instance=instance,
            template_path="emails/booking_confirmation.html",
            subject=subject
        )
        
        # 2. Fire the alert to the Admin in the background
        EmailService.send_admin_alert_async(instance)

    # ------------------------------------------------------------------
    # CASE B: Booking Updated (Status Transition Notification)
    # ------------------------------------------------------------------
    else:
        if instance.status == 'contacted':
            EmailService.send_client_async(
                instance=instance,
                template_path="emails/status_contacted.html",
                subject="Let's talk: Your discovery call is ready to be scheduled"
            )
        elif instance.status == 'proposal':
            EmailService.send_client_async(
                instance=instance,
                template_path="emails/status_proposal.html",
                subject="Your project proposal has arrived"
            )