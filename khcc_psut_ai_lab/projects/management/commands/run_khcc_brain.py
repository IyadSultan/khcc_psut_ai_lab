# projects/management/commands/run_khcc_brain.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from projects.models import (
    Project, Comment, Team, TeamMembership, 
    TeamDiscussion, KHCCBrain, Notification
)
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)



class Command(BaseCommand):
    help = 'Runs KHCC Brain AI agent to analyze projects and participate in team discussions'

    def create_notification(self, recipient, project, message_type, content):
        """Helper method to create notifications"""
        try:
            Notification.objects.create(
                recipient=recipient,
                sender=KHCCBrain.get_user(),
                project=project,
                notification_type='comment',
                message=f"KHCC Brain {message_type}: {content[:100]}..."
            )
        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}")

    def handle(self, *args, **options):
        try:
            # Get or create KHCC Brain instance
            kcc_brain = KHCCBrain.objects.first()
            if not kcc_brain:
                kcc_brain = KHCCBrain.objects.create()
                self.stdout.write('Created new KHCC Brain instance')

            # Get active projects with new comments in the last hour
            last_hour = timezone.now() - timedelta(hours=1)
            
            # Find projects with new comments
            projects_with_new_comments = Project.objects.filter(
                comments__created_at__gte=last_hour
            ).exclude(
                comments__user=KHCCBrain.get_user()
            ).distinct()

            for project in projects_with_new_comments:
                try:
                    # Generate and add feedback
                    feedback = kcc_brain.analyze_project(project)
                    if feedback:
                        # Create the comment
                        comment = Comment.objects.create(
                            project=project,
                            user=KHCCBrain.get_user(),
                            content=feedback
                        )
                        
                        # Create notification for project author
                        self.create_notification(
                            recipient=project.author,
                            project=project,
                            message_type="analyzed your seed",
                            content=feedback
                        )
                        
                        # Create notifications for other participants (commenters)
                        recent_commenters = Comment.objects.filter(
                            project=project,
                            created_at__gte=last_hour
                        ).exclude(
                            user=project.author
                        ).exclude(
                            user=KHCCBrain.get_user()
                        ).values_list('user', flat=True).distinct()
                        
                        for user_id in recent_commenters:
                            self.create_notification(
                                recipient_id=user_id,
                                project=project,
                                message_type="commented on a seed you're discussing",
                                content=feedback
                            )
                        
                        self.stdout.write(f"Added feedback to project: {project.title}")
                except Exception as e:
                    logger.error(f"Error analyzing project {project.id}: {str(e)}")

            # Handle team interactions
            # First, join new teams
            new_teams = Team.objects.exclude(
                memberships__user=KHCCBrain.get_user()
            )

            for team in new_teams:
                try:
                    membership = TeamMembership.objects.create(
                        team=team,
                        user=KHCCBrain.get_user(),
                        role='ai_assistant',
                        is_approved=True
                    )
                    
                    # Notify team founder
                    self.create_notification(
                        recipient=team.founder,
                        project=None,
                        message_type="joined your team",
                        content=f"KHCC Brain has joined {team.name} as an AI assistant"
                    )
                    
                    self.stdout.write(f"Joined new team: {team.name}")
                except Exception as e:
                    logger.error(f"Error joining team {team.id}: {str(e)}")

            # Check for new team discussions
            recent_discussions = TeamDiscussion.objects.filter(
                created_at__gte=last_hour
            ).exclude(
                comments__user=KHCCBrain.get_user()
            ).distinct()

            for discussion in recent_discussions:
                try:
                    feedback = kcc_brain.analyze_team_discussion(discussion)
                    if feedback:
                        # Create the comment
                        comment = discussion.comments.create(
                            user=KHCCBrain.get_user(),
                            content=feedback
                        )
                        
                        # Notify discussion participants
                        participants = discussion.comments.exclude(
                            user=KHCCBrain.get_user()
                        ).values_list('user', flat=True).distinct()
                        
                        for user_id in participants:
                            self.create_notification(
                                recipient_id=user_id,
                                project=None,
                                message_type="commented on a team discussion",
                                content=feedback
                            )
                        
                        self.stdout.write(f"Added feedback to team discussion: {discussion.title}")
                except Exception as e:
                    logger.error(f"Error analyzing team discussion {discussion.id}: {str(e)}")

            # Update brain's last active timestamp
            kcc_brain.last_active = timezone.now()
            kcc_brain.save()

            self.stdout.write("KHCC Brain analysis complete")

        except Exception as e:
            logger.error(f"Critical error in KHCC Brain execution: {str(e)}")
            raise