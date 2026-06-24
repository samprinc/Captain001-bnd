import threading
import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailThread(threading.Thread):
    def __init__(self, subject, plain_message, html_message, recipient_list, from_email):
        self.subject = subject
        self.plain_message = plain_message
        self.html_message = html_message
        self.recipient_list = recipient_list
        self.from_email = from_email
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.plain_message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
                html_message=self.html_message,
                fail_silently=False
            )
            logger.info(f"✅ Background Email Success: Sent to {self.recipient_list}")
        except Exception as e:
            logger.error(f"❌ Background Email Failed: Could not send to {self.recipient_list}. Error: {str(e)}")


class EmailService:
    @staticmethod
    def send_client_async(instance, template_path, subject):
        """Sends the beautifully formatted HTML email to the actual client."""
        try:
            context = {
                "name": instance.name,
                "service": instance.service_requested,
                "budget": instance.budget,
                "details": instance.details,
                "ref_number": getattr(instance, 'reference_number', f"CAP-2026-{instance.id:04d}"),
            }
            
            html = render_to_string(template_path, context)
            plain_text = strip_tags(html)
            
            # Send to the CLIENT's email address (instance.email)
            EmailThread(
                subject=f"{subject} | Captain 001 Media",
                plain_message=plain_text,
                html_message=html,
                recipient_list=[instance.email], 
                from_email=settings.DEFAULT_FROM_EMAIL
            ).start()
            
        except Exception as e:
            logger.error(f"Failed to spawn client email thread: {str(e)}")

    @staticmethod
    def send_admin_alert_async(instance):
        """Sends a quick, structured plain-text alert to the Agency Admin (You)."""
        try:
            subject = f"🚨 New Lead Alert: {instance.name} - {instance.service_requested}"
            
            # Structured layout so you can read it instantly on your phone
            message = (
                f"NEW BOOKING REQUEST\n"
                f"-----------------------------------------\n"
                f"Name:    {instance.name}\n"
                f"Email:   {instance.email}\n"
                f"Phone:   {getattr(instance, 'phone', 'Not provided')}\n"
                f"Service: {instance.service_requested}\n"
                f"Budget:  {instance.budget}\n"
                f"-----------------------------------------\n\n"
                f"PROJECT DETAILS:\n"
                f"{instance.details}\n"
            )
            
            # Send to YOU (using the environment variable)
            EmailThread(
                subject=subject,
                plain_message=message,
                html_message=None, # No HTML needed for internal alerts
                recipient_list=[settings.AGENCY_ADMIN_EMAIL], 
                from_email=settings.DEFAULT_FROM_EMAIL
            ).start()
        except Exception as e:
            logger.error(f"Failed to spawn admin alert thread: {str(e)}")