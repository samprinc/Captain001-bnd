from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Post, Subscriber

@receiver(post_save, sender=Post)
def notify_on_publish(sender, instance, created, **kwargs):

    try:
        old_instance = Post.objects.get(pk=instance.pk)
    except Post.DoesNotExist:
        old_instance = None

    just_published = (
        instance.is_published and
        (not old_instance or not old_instance.is_published)
    )

    if just_published:
        subject = f"📰 New Post Published: {instance.title}"
        plain_message = f"{instance.title}\n\n{instance.content[:200]}...\nVisit the site to read more."
        from_email = settings.DEFAULT_FROM_EMAIL
        post_url = f"https://yourdomain.com/posts/{instance.id}"  # ✅ Update your domain here

        html_content = f"""
        <div style="font-family:Arial,sans-serif;line-height:1.6;">
          <h2>{instance.title}</h2>
          <p>{instance.content[:200]}...</p>
          <a href="{post_url}" style="
            display:inline-block;
            padding:10px 20px;
            background-color:#007BFF;
            color:#ffffff;
            text-decoration:none;
            border-radius:5px;
          ">Read Full Article</a>
        </div>
        """

        # Notify Admins
        admin_emails = [admin[1] for admin in settings.ADMINS]
        if admin_emails:
            msg = EmailMultiAlternatives(subject, plain_message, from_email, admin_emails)
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

        # Notify Author
        if hasattr(instance, "author") and instance.author and instance.author.email:
            msg = EmailMultiAlternatives(subject, plain_message, from_email, [instance.author.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

        # Notify Subscribers
        subscriber_emails = Subscriber.objects.values_list('email', flat=True)
        if subscriber_emails:
            msg = EmailMultiAlternatives(subject, plain_message, from_email, list(subscriber_emails))
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
