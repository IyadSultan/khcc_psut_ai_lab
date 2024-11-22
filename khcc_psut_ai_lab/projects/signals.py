from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import TeamMembership, TeamDiscussion, TeamComment, TeamAnalytics
from .utils.team_emails import send_team_notification_email, send_role_change_notification

@receiver(post_save, sender=TeamDiscussion)
def handle_new_discussion(sender, instance, created, **kwargs):
    if created:
        # Update analytics
        analytics = instance.team.analytics
        analytics.total_discussions = F('total_discussions') + 1
        analytics.discussions_this_week = F('discussions_this_week') + 1
        analytics.discussions_this_month = F('discussions_this_month') + 1
        analytics.save()
        
        # Notify team members
        for membership in instance.team.memberships.filter(
            is_approved=True,
            # notification_preferences__in_app_notifications=True
        ).exclude(user=instance.author):
            send_team_notification_email(
                membership.user,
                instance.team,
                'discussion',
                {'discussion': instance}
            )

@receiver(post_save, sender=TeamComment)
def handle_new_comment(sender, instance, created, **kwargs):
    if created:
        # Update analytics
        analytics = instance.discussion.team.analytics
        analytics.total_comments = F('total_comments') + 1
        analytics.comments_this_week = F('comments_this_week') + 1
        analytics.comments_this_month = F('comments_this_month') + 1
        analytics.save()
        
        # Notify team members
        for membership in instance.discussion.team.memberships.filter(
            is_approved=True,
            # notification_preferences__in_app_notifications=True
        ).exclude(user=instance.author):
            send_team_notification_email(
                membership.user,
                instance.discussion.team,
                'comment',
                {'comment': instance}
            )

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


from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project
from .services import OpenAITaggingService

@receiver(pre_save, sender=Project)
def auto_generate_tags(sender, instance, **kwargs):
    """
    Signal handler to automatically generate tags before saving a Project
    
    Only generates tags if:
    1. No tags are currently set
    2. The project is being created for the first time
    """
    if not instance.pk and not instance.tags:  # New project without tags
        tagging_service = OpenAITaggingService()
        generated_tags = tagging_service.generate_tags(
            title=instance.title,
            description=instance.description
        )
        if generated_tags:
            instance.tags = generated_tags