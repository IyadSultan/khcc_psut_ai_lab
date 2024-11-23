from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db.models import F
from .models import (
    TeamMembership,
    TeamDiscussion,
    TeamComment,
    TeamAnalytics,
    Project
)
from .utils.team_emails import send_team_notification_email, send_role_change_notification
from .services import OpenAITaggingService

@receiver(post_save, sender=TeamDiscussion)
def handle_new_discussion(sender, instance, created, **kwargs):
    """Handle notifications for new team discussions"""
    if created:
        # Get team members to notify
        members = instance.team.memberships.filter(
            is_approved=True,
            receive_notifications=True
        ).exclude(user=instance.author)
        
        # Send notifications to each member
        for membership in members:
            try:
                send_team_notification_email(
                    user=membership.user,
                    team=instance.team,
                    notification_type='discussion',
                    context={
                        'discussion': instance
                    }
                )
            except Exception as e:
                print(f"Error sending notification to {membership.user}: {str(e)}")

@receiver(post_save, sender=TeamComment)
def handle_new_comment(sender, instance, created, **kwargs):
    """Handle notifications for new team comments"""
    if created:
        # Get team members to notify
        members = instance.discussion.team.memberships.filter(
            is_approved=True,
            receive_notifications=True
        ).exclude(user=instance.author)
        
        # Send notifications to each member
        for membership in members:
            try:
                send_team_notification_email(
                    user=membership.user,
                    team=instance.discussion.team,
                    notification_type='comment',
                    context={
                        'comment': instance,
                        'discussion': instance.discussion
                    }
                )
            except Exception as e:
                print(f"Error sending notification to {membership.user}: {str(e)}")

@receiver(post_save, sender=TeamMembership)
def handle_membership_changes(sender, instance, created, **kwargs):
    if not created and instance.tracker.has_changed('role'):
        send_role_change_notification(
            instance.user,
            instance.team,
            instance.get_role_display()
        )

@receiver(post_delete, sender=TeamMembership)
def handle_member_removal(sender, instance, **kwargs):
    # Update analytics
    instance.team.analytics.update_stats()



@receiver(pre_save, sender=Project)
def auto_generate_tags(sender, instance, **kwargs):
    """
    Signal handler to automatically generate tags before saving a Project
    
    Only generates tags if:
    1. No tags are currently set
    2. The project is being created for the first time
    """
    if not instance.pk:  # New project without tags
        tagging_service = OpenAITaggingService()
        generated_tags = tagging_service.generate_tags(
            title=instance.title,
            description=instance.description
        )
        if generated_tags:
            # Combine existing and generated tags
            existing_tags = instance.tags.split(',') if instance.tags else []
            new_tags = generated_tags.split(',')
            combined_tags = list(set(existing_tags + new_tags))  # Remove duplicates
            instance.tags = ','.join(tag.strip() for tag in combined_tags if tag.strip())