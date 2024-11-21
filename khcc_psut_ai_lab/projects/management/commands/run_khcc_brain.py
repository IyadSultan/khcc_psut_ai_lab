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

    def join_new_teams(self, kcc_brain_user):
        """Helper method to join new teams"""
        # Get all teams KHCC Brain hasn't joined yet
        new_teams = Team.objects.exclude(
            memberships__user=kcc_brain_user
        )
        
        for team in new_teams:
            try:
                # Join team
                membership = TeamMembership.objects.create(
                    team=team,
                    user=kcc_brain_user,
                    role='member',
                    is_approved=True
                )
                
                # Create welcome message
                welcome_message = f"""
Hello {team.name} team! 👋

I'm KHCC Brain, your AI research assistant, and I'm excited to join this team. I'm here to help with:

• Analyzing discussions and providing insights
• Suggesting potential research directions
• Offering relevant healthcare AI perspectives
• Identifying collaboration opportunities

Feel free to mention me in any discussions where you'd like my input. I'll be actively monitoring our team's conversations and contributing where I can help most.

Looking forward to collaborating with everyone!

Best regards,
KHCC Brain 🤖
                """
                
                discussion = TeamDiscussion.objects.create(
                    team=team,
                    author=kcc_brain_user,
                    title="KHCC Brain Introduction",
                    content=welcome_message
                )
                
                self.stdout.write(f"Successfully joined team and posted welcome message: {team.name}")
                
            except Exception as e:
                logger.error(f"Error joining team {team.id}: {str(e)}")

    def handle(self, *args, **options):
        try:
            # Get or create KHCC Brain instance
            kcc_brain = KHCCBrain.objects.first()
            if not kcc_brain:
                kcc_brain = KHCCBrain.objects.create()
                self.stdout.write('Created new KHCC Brain instance')

            # Get KHCC Brain user
            kcc_brain_user = KHCCBrain.get_user()
            
            # First, handle team memberships
            self.join_new_teams(kcc_brain_user)

            # Get active projects with new comments in the last hour
            last_hour = timezone.now() - timedelta(hours=1)
            
            # Find projects with new comments
            projects_with_new_comments = Project.objects.filter(
                comments__created_at__gte=last_hour
            ).exclude(
                comments__user=kcc_brain_user
            ).distinct()

            for project in projects_with_new_comments:
                try:
                    # Generate and add feedback
                    feedback = kcc_brain.analyze_project(project)
                    if feedback:
                        comment = Comment.objects.create(
                            project=project,
                            user=kcc_brain_user,
                            content=feedback
                        )
                        
                        # Notify project author
                        Notification.objects.create(
                            recipient=project.author,
                            sender=kcc_brain_user,
                            project=project,
                            notification_type='comment',
                            message=f"KHCC Brain analyzed your seed: {feedback[:100]}..."
                        )
                        
                        self.stdout.write(f"Added feedback to project: {project.title}")
                except Exception as e:
                    logger.error(f"Error analyzing project {project.id}: {str(e)}")

            # Check for new team discussions
            recent_discussions = TeamDiscussion.objects.filter(
                Q(created_at__gte=last_hour) |
                Q(comments__created_at__gte=last_hour)
            ).exclude(
                comments__user=kcc_brain_user
            ).distinct()

            for discussion in recent_discussions:
                try:
                    feedback = kcc_brain.analyze_team_discussion(discussion)
                    if feedback:
                        comment = discussion.comments.create(
                            user=kcc_brain_user,
                            content=feedback
                        )
                        
                        # Notify discussion participants
                        participants = discussion.team.memberships.filter(
                            is_approved=True
                        ).exclude(
                            user=kcc_brain_user
                        ).values_list('user', flat=True)
                        
                        for user_id in participants:
                            Notification.objects.create(
                                recipient_id=user_id,
                                sender=kcc_brain_user,
                                notification_type='team_comment',
                                message=f"KHCC Brain commented on team discussion: {discussion.title}"
                            )
                        
                        self.stdout.write(f"Added feedback to team discussion: {discussion.title}")
                except Exception as e:
                    logger.error(f"Error analyzing team discussion {discussion.id}: {str(e)}")

            # Update brain's last active timestamp
            kcc_brain.last_active = timezone.now()
            kcc_brain.save()

            self.stdout.write(
                self.style.SUCCESS("KHCC Brain analysis complete")
            )

        except Exception as e:
            logger.error(f"Critical error in KHCC Brain execution: {str(e)}")
            raise