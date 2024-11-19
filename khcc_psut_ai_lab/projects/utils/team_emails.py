from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_team_notification_email(user, team, notification_type, context=None):
    """Send email notifications for team activities"""
    if context is None:
        context = {}
    
    context.update({
        'user': user,
        'team': team,
        'site_url': settings.SITE_URL
    })
    
    templates = {
        'discussion': 'emails/team_discussion.html',
        'comment': 'emails/team_comment.html',
        'role_change': 'emails/team_role_change.html',
        'invitation': 'emails/team_invitation.html'
    }
    
    template = templates.get(notification_type)
    if not template:
        return
        
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    
    subject = f"New activity in {team.name} - {notification_type.title()}"
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

def send_team_invitation_email(user, team, inviter):
    """Send email for team invitation"""
    context = {
        'user': user,
        'team': team,
        'inviter': inviter,
        'site_url': settings.SITE_URL
    }
    
    html_message = render_to_string('emails/team_invitation.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        f"Invitation to join {team.name}",
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

def send_role_change_notification(user, team, new_role):
    """Send email for role changes"""
    context = {
        'user': user,
        'team': team,
        'new_role': new_role,
        'site_url': settings.SITE_URL
    }
    
    html_message = render_to_string('emails/team_role_change.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        f"Role update in {team.name}",
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )