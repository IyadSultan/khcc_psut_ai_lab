# projects/utils/emails.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_notification_email(notification):
    """Send email for a new notification"""
    subject = f'New notification from {settings.SITE_NAME}'
    context = {
        'notification': notification,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/notification.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [notification.recipient.email],
        html_message=html_message,
        fail_silently=True
    )

def send_welcome_email(user):
    """Send welcome email to new users"""
    subject = f'Welcome to {settings.SITE_NAME}'
    context = {
        'user': user,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

def send_comment_notification(comment):
    """Send email notification for new comments"""
    subject = f'New comment on your project - {settings.SITE_NAME}'
    context = {
        'comment': comment,
        'project': comment.project,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/project_comment.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [comment.project.author.email],
        html_message=html_message,
        fail_silently=True
    )

def send_clap_notification(clap):
    """Send email notification for new claps"""
    subject = f'Someone appreciated your project - {settings.SITE_NAME}'
    context = {
        'clap': clap,
        'project': clap.project,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/project_clap.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [clap.project.author.email],
        html_message=html_message,
        fail_silently=True
    )