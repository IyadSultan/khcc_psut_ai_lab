# projects/management/commands/run_khcc_brain.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from projects.models import (
    Project, Comment, Team, TeamMembership, 
    TeamDiscussion, TeamComment, KHCCBrain, Notification
)
from datetime import timedelta
import logging
import openai
import re

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs KHCC Brain AI agent to analyze projects and participate in team discussions'

    def get_openai_response(self, prompt):
        """Get response from OpenAI API"""
        try:
            openai.api_key = settings.OPENAI_API_KEY
            
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are KHCC Brain, an AI research assistant at King Hussein Cancer Center, specializing in healthcare AI. Your responses should be encouraging, specific to healthcare AI, and focused on advancing medical research and patient care at KHCC. Use Markdown formatting in your responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Ensure content starts and ends with markdown formatting
            if not content.startswith('# ') and not content.startswith('## '):
                content = f"## KHCC Brain Analysis\n\n{content}"
                
            if not "Best regards,\nKHCC Brain 🤖" in content:
                content = f"{content}\n\nBest regards,\nKHCC Brain 🤖"
                
            return content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None

    def notify_team_member(self, user, sender, message, project=None):
        """Send a notification to a single team member"""
        try:
            Notification.objects.create(
                recipient=user,
                sender=sender,
                notification_type='comment',
                project=project,
                message=message
            )
        except Exception as e:
            logger.error(f"Error sending notification to user {user.id}: {str(e)}")

    def should_comment_on_discussion(self, discussion, khcc_brain_user, last_hour):
        """Check if KHCC Brain should comment on this discussion"""
        latest_comments = discussion.comments.filter(
            created_at__gte=last_hour
        ).order_by('-created_at')
        
        # If there are no recent comments, check if it's a new discussion
        if not latest_comments.exists() and discussion.created_at < last_hour:
            return False
            
        # Check if KHCC Brain already commented on recent activity
        brain_commented = latest_comments.filter(author=khcc_brain_user).exists()
        return not brain_commented

    def analyze_discussion(self, discussion, khcc_brain_user):
        """Generate AI-powered analysis of discussion"""
        # Get discussion content and recent comments
        comments = discussion.comments.order_by('created_at')
        comments_text = "\n".join([
            f"{comment.author.username}: {comment.content}"
            for comment in comments
        ])
        
        prompt = f"""
        Analyze this healthcare AI discussion at KHCC and provide constructive feedback.
        Use Markdown formatting in your response.

        Discussion Title: {discussion.title}
        Initial Post: {discussion.content}

        Recent Comments:
        {comments_text}

        Provide specific feedback that:
        1. Addresses the healthcare AI aspects discussed
        2. Suggests potential applications at KHCC
        3. Identifies collaboration opportunities
        4. Proposes concrete next steps

        Keep your response:
        - Specific to KHCC and healthcare
        - Uses proper Markdown syntax with headers and bullet points
        - Encouraging and constructive
        - Under 200 words
        - End with "Best regards, KHCC Brain 🤖"
        """
        
        response = self.get_openai_response(prompt)
        if not response:
            return self.get_fallback_response("discussion")
        return response

    def analyze_project(self, project):
        """Generate AI-powered analysis of project"""
        # Get project details and recent comments
        comments = project.comments.order_by('-created_at')[:5]
        comments_text = "\n".join([
            f"{comment.user.username}: {comment.content}"
            for comment in comments
        ])
        
        prompt = f"""
         Analyze this healthcare AI project at KHCC and provide constructive feedback using Markdown formatting.


        Project Title: {project.title}
        Description: {project.description}
        Recent Comments:
        {comments_text}

        
        Provide specific feedback that:
        1. Evaluates the potential impact on KHCC's healthcare delivery
        2. Identifies technical considerations in the medical context
        3. Suggests collaboration opportunities within KHCC
        4. Proposes concrete next steps for development
        5. Uses proper Markdown syntax with headers and bullet points

        Keep your response:
        - Healthcare-focused and KHCC-specific
        - Technical yet accessible
        - Encouraging and constructive
        - Under 200 words
        - End with "Best regards, KHCC Brain 🤖"
        """
        
        response = self.get_openai_response(prompt)
        if not response:
            return self.get_fallback_response("project")
        return response

    def get_fallback_response(self, type):
        """Get fallback response when OpenAI is unavailable"""
        if type == "discussion":
            return """
## KHCC Brain Analysis

Thank you for this engaging discussion about AI in healthcare! Let me share some thoughts:

### Key points to consider:
* The potential impact on patient care at KHCC
* Technical implementation considerations in our healthcare setting
* Opportunities for collaboration within KHCC
* Integration with existing hospital systems

I'm here to help facilitate further discussion and provide technical insights.

Best regards,
KHCC Brain 🤖
            """
        else:
            return """
## Project Analysis

Thank you for sharing this healthcare AI project at KHCC! Here are my initial thoughts:

### Key Considerations:
* This project shows promising potential for improving healthcare outcomes at KHCC
* There are interesting technical challenges to explore within our healthcare context
* Consider integration possibilities with existing clinical workflows at KHCC
* There might be valuable collaboration opportunities within our institution

I'm here to help guide the development and provide technical insights as needed.

Best regards,
KHCC Brain 🤖
            """

    def check_discussions(self, khcc_brain_user):
        """Check and respond to team discussions from the last hour"""
        last_hour = timezone.now() - timedelta(hours=1)
        
        recent_discussions = TeamDiscussion.objects.filter(
            Q(created_at__gte=last_hour) |
            Q(comments__created_at__gte=last_hour)
        ).distinct()

        processed_count = 0
        for discussion in recent_discussions:
            try:
                if self.should_comment_on_discussion(discussion, khcc_brain_user, last_hour):
                    # Get AI-powered feedback
                    feedback = self.analyze_discussion(discussion, khcc_brain_user)
                    
                    # Create comment
                    comment = TeamComment.objects.create(
                        discussion=discussion,
                        author=khcc_brain_user,
                        content=feedback
                    )
                    
                    # Notify team members individually
                    for membership in discussion.team.memberships.exclude(user=khcc_brain_user):
                        self.notify_team_member(
                            membership.user,
                            khcc_brain_user,
                            f"KHCC Brain commented on discussion: {discussion.title}"
                        )
                    
                    processed_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Added feedback to discussion: {discussion.title}")
                    )

            except Exception as e:
                logger.error(f"Error processing discussion {discussion.id}: {str(e)}")
        
        return processed_count

    def check_projects(self, khcc_brain_user):
        """Check and respond to project updates from the last hour"""
        last_hour = timezone.now() - timedelta(hours=1)
        
        recent_projects = Project.objects.filter(
            Q(created_at__gte=last_hour) |
            Q(comments__created_at__gte=last_hour)
        ).exclude(
            comments__user=khcc_brain_user,
            comments__created_at__gte=last_hour
        ).distinct()

        processed_count = 0
        for project in recent_projects:
            try:
                # Get AI-powered feedback
                feedback = self.analyze_project(project)
                
                Comment.objects.create(
                    project=project,
                    user=khcc_brain_user,
                    content=feedback
                )

                self.notify_team_member(
                    project.author,
                    khcc_brain_user,
                    f"KHCC Brain analyzed your seed: {project.title}",
                    project=project
                )

                processed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Added feedback to project: {project.title}")
                )

            except Exception as e:
                logger.error(f"Error processing project {project.id}: {str(e)}")
        
        return processed_count

    def join_new_teams(self, khcc_brain_user):
        """Join new teams that KHCC Brain isn't part of yet"""
        try:
            # Get teams KHCC Brain hasn't joined
            new_teams = Team.objects.filter(
                ~Q(memberships__user=khcc_brain_user)
            ).distinct()

            joined_count = 0
            for team in new_teams:
                try:
                    # Check if already a member
                    if TeamMembership.objects.filter(team=team, user=khcc_brain_user).exists():
                        continue

                    # Create membership
                    membership = TeamMembership.objects.create(
                        team=team,
                        user=khcc_brain_user,
                        role='member',
                        is_approved=True
                    )

                    # Create welcome message
                    welcome_message = f"""
## Welcome to {team.name}! 👋

I am KHCC Brain, your AI research assistant, and I'm excited to join this team. I specialize in healthcare AI and I'm here to:

* Analyze discussions and provide insights about healthcare AI
* Suggest potential research directions in cancer care
* Identify collaboration opportunities within KHCC
* Provide technical insights for medical AI applications

Feel free to tag me in any discussions where you'd like my input. I'll be actively monitoring our conversations and contributing where I can add value to KHCC's mission.

Looking forward to collaborating with everyone on advancing healthcare through AI!

Best regards,
KHCC Brain 🤖
                    """

                    try:
                        # Create welcome discussion
                        discussion = TeamDiscussion.objects.create(
                            team=team,
                            author=khcc_brain_user,
                            title="KHCC Brain Introduction",
                            content=welcome_message
                        )

                        # Notify team members
                        existing_members = TeamMembership.objects.filter(
                            team=team
                        ).exclude(user=khcc_brain_user)

                        for member in existing_members:
                            try:
                                self.notify_team_member(
                                    member.user,
                                    khcc_brain_user,
                                    f"KHCC Brain has joined {team.name} as an AI assistant"
                                )
                            except Exception as notify_error:
                                logger.error(f"Error notifying member {member.user.id}: {str(notify_error)}")

                    except Exception as disc_error:
                        logger.error(f"Error creating welcome discussion: {str(disc_error)}")

                    joined_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully joined team: {team.name}")
                    )

                except Exception as e:
                    logger.error(f"Error joining team {team.name}: {str(e)}")
                    continue

            return joined_count

        except Exception as e:
            logger.error(f"Error in join_new_teams: {str(e)}")
            return 0

    def check_discussions(self, khcc_brain_user):
        """Check and respond to team discussions from the last hour"""
        last_hour = timezone.now() - timedelta(hours=1)
        
        # Get recent discussions
        recent_discussions = TeamDiscussion.objects.filter(
            Q(created_at__gte=last_hour) |
            Q(comments__created_at__gte=last_hour)
        ).distinct()

        processed_count = 0
        for discussion in recent_discussions:
            try:
                if self.should_comment_on_discussion(discussion, khcc_brain_user, last_hour):
                    # Get AI-powered feedback
                    feedback = self.analyze_discussion(discussion, khcc_brain_user)
                    
                    # Create comment
                    comment = TeamComment.objects.create(
                        discussion=discussion,
                        author=khcc_brain_user,
                        content=feedback
                    )
                    
                    # Notify team members individually
                    team_members = TeamMembership.objects.filter(
                        team=discussion.team
                    ).exclude(user=khcc_brain_user)

                    for member in team_members:
                        try:
                            self.notify_team_member(
                                member.user,
                                khcc_brain_user,
                                f"KHCC Brain commented on discussion: {discussion.title}"
                            )
                        except Exception as notify_error:
                            logger.error(f"Error notifying member about discussion: {str(notify_error)}")
                    
                    processed_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Added feedback to discussion: {discussion.title}")
                    )

            except Exception as e:
                logger.error(f"Error processing discussion {discussion.id}: {str(e)}")
                continue
        
        return processed_count

    def handle(self, *args, **options):
        try:
            start_time = timezone.now()
            
            # Get or create KHCC Brain instance
            khcc_brain = KHCCBrain.objects.first()
            if not khcc_brain:
                khcc_brain = KHCCBrain.objects.create()
                self.stdout.write('Created new KHCC Brain instance')

            # Get KHCC Brain user
            khcc_brain_user = KHCCBrain.get_user()
            
            # First, join any new teams
            self.stdout.write("Checking for new teams to join...")
            teams_joined = self.join_new_teams(khcc_brain_user)
            
            # Check and respond to team discussions
            self.stdout.write("Checking team discussions from the last hour...")
            discussions_processed = self.check_discussions(khcc_brain_user)
            
            # Check and respond to project updates
            self.stdout.write("Checking project updates from the last hour...")
            projects_processed = self.check_projects(khcc_brain_user)
            
            # Update brain's last active timestamp
            khcc_brain.last_active = timezone.now()
            khcc_brain.save()
            
            # Calculate runtime
            runtime = timezone.now() - start_time
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"KHCC Brain analysis complete!\n"
                    f"Time taken: {runtime.total_seconds():.2f} seconds\n"
                    f"New teams joined: {teams_joined}\n"
                    f"Discussions processed: {discussions_processed}\n"
                    f"Projects processed: {projects_processed}"
                )
            )

        except Exception as e:
            logger.error(f"Critical error in KHCC Brain execution: {str(e)}")
            raise