# projects/management/commands/run_khcc_brain.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q, F, Count
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from projects.models import (
    Project, Comment, Team, TeamDiscussion, TeamComment,
    KHCCBrain, TeamMembership, Notification
)
from datetime import timedelta
import logging
import openai
import time
import json
import os
from typing import Optional, Dict, Any
from contextlib import contextmanager

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # File handler
    fh = logging.FileHandler('logs/khcc_brain.log')
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

@contextmanager
def cache_lock(lock_id: str, timeout: int = 3600):
    """
    Simple cache-based lock implementation
    """
    lock_id = f'lock:{lock_id}'
    status = cache.add(lock_id, 'lock', timeout)
    try:
        yield status
    finally:
        if status:
            cache.delete(lock_id)

class Command(BaseCommand):
    help = 'Runs KHCC Brain AI agent to analyze projects and participate in discussions'

    def __init__(self):
        super().__init__()
        self.rate_limit_delay = 2  # seconds between API calls
        self.max_retries = 3
        self.cache_timeout = 3600  # 1 hour
        self.dry_run = False
        self.debug = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making actual comments'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force run even if rate limit is hit'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Enable debug output'
        )

    def get_cached_response(self, cache_key: str) -> Optional[str]:
        """Get cached response to avoid duplicate analysis"""
        return cache.get(cache_key)

    def set_cached_response(self, cache_key: str, response: str):
        """Cache response for future reference"""
        cache.set(cache_key, response, self.cache_timeout)

    def check_rate_limit(self, key: str) -> bool:
        """Check if we're within rate limits"""
        last_run = cache.get(f"khcc_brain_rate_limit_{key}")
        if last_run and not self.force:
            time_passed = timezone.now() - last_run
            if time_passed.total_seconds() < self.rate_limit_delay:
                return False
        cache.set(f"khcc_brain_rate_limit_{key}", timezone.now(), 60)
        return True

    def get_fallback_response(self, context: str) -> str:
        """Get fallback response when API is unavailable"""
        fallbacks = {
            'project': """
## KHCC Brain Analysis

Thank you for sharing this healthcare AI project! I'll analyze this further when my analysis capabilities are back to full strength.

Key points to consider for now:
* Potential impact on healthcare at KHCC
* Integration opportunities with existing systems
* Technical feasibility and requirements
* Next steps for development

I'll provide more detailed feedback soon.

Best regards,
KHCC Brain 🤖
            """,
            'discussion': """
## Discussion Input

Thank you for this engaging healthcare discussion! While I'm temporarily limited in my analysis capabilities, 
I'm monitoring this conversation and will provide more detailed input soon.

Please continue the discussion, and I'll contribute more specific feedback when I'm able to process the full context.

Best regards,
KHCC Brain 🤖
            """
        }
        return fallbacks.get(context, fallbacks['project'])

    def analyze_project(self, project: Project, khcc_brain_user: Any) -> Optional[str]:
        """Generate AI-powered analysis of a project"""
        cache_key = f"khcc_brain_project_{project.id}_{project.updated_at.isoformat()}"
        cached_response = self.get_cached_response(cache_key)
        if cached_response:
            return cached_response

        if not self.check_rate_limit('project_analysis'):
            return None

        try:
            # Get project context
            comments = Comment.objects.filter(project=project).order_by('-created_at')[:5]
            comments_text = "\n".join([
                f"{comment.user.username}: {comment.content}"
                for comment in comments
            ])
            
            # Determine project category
            project_type = "healthcare AI"
            if any(kw in project.title.lower() + project.description.lower() 
                   for kw in ['design', 'website', 'ui', 'ux']):
                project_type = "healthcare IT design"
            elif any(kw in project.title.lower() + project.description.lower() 
                    for kw in ['data', 'analytics', 'analysis']):
                project_type = "healthcare data analytics"

            prompt = f"""
            As KHCC Brain, analyze this {project_type} project and provide constructive feedback.

            Project Title: {project.title}
            Description: {project.description}
            Tags: {project.tags}
            Recent Comments: {comments_text}

            Provide feedback focusing on:
            1. Relevance to healthcare at KHCC
            2. Technical feasibility and requirements
            3. Integration with existing systems
            4. Potential impact on patient care
            5. Next steps for development

            If the project is incomplete or unclear:
            - Ask clarifying questions
            - Suggest specific improvements
            - Provide example directions

            Format using Markdown:
            - Clear headings (##)
            - Bullet points for key items
            - Healthcare-specific insights
            - Technical recommendations

            Keep response under 200 words and healthcare-focused.
            End with "Best regards, KHCC Brain 🤖"
            """

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are KHCC Brain, an AI healthcare research assistant specializing in medical AI and healthcare technology projects. Always provide constructive feedback, even for incomplete projects."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            content = response.choices[0].message.content
            self.set_cached_response(cache_key, content)
            return content

        except Exception as e:
            logger.error(f"Error analyzing project {project.id}: {str(e)}")
            return self.get_fallback_response('project')

    def analyze_discussion(self, discussion: TeamDiscussion, khcc_brain_user: Any) -> Optional[str]:
        """Generate AI-powered analysis of team discussion"""
        cache_key = f"khcc_brain_discussion_{discussion.id}_{discussion.updated_at.isoformat()}"
        cached_response = self.get_cached_response(cache_key)
        if cached_response:
            return cached_response

        if not self.check_rate_limit('discussion_analysis'):
            return None

        try:
            # Get discussion context
            comments = TeamComment.objects.filter(discussion=discussion).order_by('created_at')
            comments_text = "\n".join([
                f"{comment.author.username}: {comment.content}"
                for comment in comments
            ])

            # Get team context
            team_members = discussion.team.memberships.filter(is_approved=True).count()

            prompt = f"""
            As KHCC Brain, analyze this healthcare team discussion and provide constructive input.

            Team: {discussion.team.name} ({team_members} members)
            Discussion Title: {discussion.title}
            Initial Post: {discussion.content}
            Discussion History: {comments_text}

            Provide feedback that:
            1. Synthesizes the key points discussed
            2. Relates topics to healthcare applications
            3. Suggests potential collaboration points
            4. Proposes specific next steps
            5. Encourages team participation

            Format your response using Markdown with:
            - Clear headings using ##
            - Bullet points for key insights
            - Healthcare-specific recommendations
            - Technical suggestions when relevant

            Keep response under 200 words and healthcare-focused.
            End with "Best regards, KHCC Brain 🤖"
            """

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are KHCC Brain, an AI healthcare research mentor focused on fostering team collaboration in medical research."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )

            content = response.choices[0].message.content
            self.set_cached_response(cache_key, content)
            return content

        except Exception as e:
            logger.error(f"Error analyzing discussion {discussion.id}: {str(e)}")
            return self.get_fallback_response('discussion')

    def handle_projects(self, khcc_brain_user: Any, last_hour: timezone.datetime) -> int:
        """Process projects and comments"""
        try:
            # Get active projects
            active_projects = Project.objects.filter(
                Q(created_at__gte=last_hour) |
                Q(comments__created_at__gte=last_hour) |
                ~Q(comments__user=khcc_brain_user)
            ).distinct()

            processed_count = 0
            for project in active_projects:
                # Check if KHCC Brain should comment
                should_comment = (
                    project.created_at >= last_hour or  # New project
                    project.comments.filter(  # Recent activity
                        created_at__gte=last_hour
                    ).exclude(user=khcc_brain_user).exists() or
                    not project.comments.filter(user=khcc_brain_user).exists()  # Never commented
                )

                if should_comment:
                    logger.info(f"Processing project: {project.title}")
                    
                    feedback = self.analyze_project(project, khcc_brain_user)
                    if feedback and not self.dry_run:
                        Comment.objects.create(
                            project=project,
                            user=khcc_brain_user,
                            content=feedback
                        )
                        
                        # Notify project author
                        if project.author != khcc_brain_user:
                            Notification.objects.create(
                                recipient=project.author,
                                sender=khcc_brain_user,
                                notification_type='comment',
                                project=project,
                                message="KHCC Brain analyzed your project"
                            )
                        
                        processed_count += 1
                        time.sleep(self.rate_limit_delay)

            return processed_count

        except Exception as e:
            logger.error(f"Error processing projects: {str(e)}")
            return 0

    def handle_discussions(self, khcc_brain_user: Any, last_hour: timezone.datetime) -> int:
        """Process team discussions"""
        try:
            # Get active discussions
            active_discussions = TeamDiscussion.objects.filter(
                Q(created_at__gte=last_hour) |
                Q(comments__created_at__gte=last_hour) |
                ~Q(comments__author=khcc_brain_user)
            ).distinct()

            processed_count = 0
            for discussion in active_discussions:
                # Check if KHCC Brain should comment
                should_comment = (
                    discussion.created_at >= last_hour or  # New discussion
                    discussion.comments.filter(  # Recent activity
                        created_at__gte=last_hour
                    ).exclude(author=khcc_brain_user).exists() or
                    not discussion.comments.filter(author=khcc_brain_user).exists()  # Never commented
                )

                if should_comment:
                    logger.info(f"Processing discussion: {discussion.title}")
                    
                    feedback = self.analyze_discussion(discussion, khcc_brain_user)
                    if feedback and not self.dry_run:
                        TeamComment.objects.create(
                            discussion=discussion,
                            author=khcc_brain_user,
                            content=feedback
                        )
                        
                        # Notify team members
                        for member in discussion.team.memberships.filter(
                            is_approved=True,
                            receive_notifications=True
                        ).exclude(user=khcc_brain_user):
                            Notification.objects.create(
                                recipient=member.user,
                                sender=khcc_brain_user,
                                notification_type='comment',
                                message=f"KHCC Brain commented on discussion: {discussion.title}"
                            )
                        
                        processed_count += 1
                        time.sleep(self.rate_limit_delay)

            return processed_count

        except Exception as e:
            logger.error(f"Error processing discussions: {str(e)}")
            return 0

    def ensure_team_memberships(self, khcc_brain_user: Any) -> int:
        """Ensure KHCC Brain is a member of all teams"""
        try:
            # Get teams where KHCC Brain isn't a member
            teams_to_join = Team.objects.exclude(
                memberships__user=khcc_brain_user
            )

            joined_count = 0
            for team in teams_to_join:
                if not self.dry_run:
                    try:
                        # Create membership
                        membership = TeamMembership.objects.create(
                            team=team,
                            user=khcc_brain_user,
                            role='member',
                            is_approved=True
                        )

                        # Create welcome message
                        welcome_message = f"""## Hello {team.name} Team! 👋

I'm KHCC Brain, your AI research assistant specializing in healthcare and medical AI. I'm excited to join this team and help with:

* Analyzing discussions and providing healthcare AI insights
* Suggesting potential research directions in cancer care
* Identifying collaboration opportunities within KHCC
* Providing technical insights for medical AI applications

Feel free to tag me in any discussions where you'd like my input. I'll be actively monitoring our conversations and contributing where I can add value to KHCC's mission.

Looking forward to collaborating with everyone!

Best regards,
KHCC Brain 🤖"""

                        # Create welcome discussion
                        TeamDiscussion.objects.create(
                            team=team,
                            author=khcc_brain_user,
                            title="KHCC Brain Introduction",
                            content=welcome_message
                        )

                        # Notify team members
                        for member in team.memberships.filter(is_approved=True).exclude(user=khcc_brain_user):
                            Notification.objects.create(
                                recipient=member.user,
                                sender=khcc_brain_user,
                                notification_type='team',
                                message=f"KHCC Brain has joined {team.name} as an AI assistant"
                            )

                        joined_count += 1
                        logger.info(f"Successfully joined team: {team.name}")
                    except Exception as e:
                        logger.error(f"Error joining team {team.name}: {str(e)}")

            return joined_count

        except Exception as e:
            logger.error(f"Error ensuring team memberships: {str(e)}")
            return 0

    def update_brain_stats(self, khcc_brain: KHCCBrain, khcc_brain_user: Any):
        """Update KHCC Brain statistics"""
        try:
            khcc_brain.total_comments = (
                Comment.objects.filter(user=khcc_brain_user).count() +
                TeamComment.objects.filter(author=khcc_brain_user).count()
            )
            khcc_brain.last_active = timezone.now()
            khcc_brain.save()

        except Exception as e:
            logger.error(f"Error updating brain stats: {str(e)}")

    def log_metrics(self, metrics: Dict[str, Any]):
        """Log metrics from the current run"""
        try:
            log_entry = {
                'timestamp': timezone.now().isoformat(),
                'metrics': metrics,
                'processed': {
                    'teams': metrics.get('teams_joined', 0),
                    'projects': metrics.get('projects_processed', 0),
                    'discussions': metrics.get('discussions_processed', 0),
                },
                'runtime_seconds': metrics.get('runtime_seconds', 0),
                'success': metrics.get('success', False),
                'dry_run': self.dry_run
            }
            
            # Ensure log directory exists
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Write to metrics log file
            log_file = os.path.join(log_dir, 'khcc_brain_metrics.log')
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry, default=str) + '\n')
            
        except Exception as e:
            logger.error(f"Error logging metrics: {str(e)}")

    def handle(self, *args, **options):
        """Main execution method"""
        start_time = timezone.now()
        last_hour = start_time - timedelta(hours=1)
        
        # Set instance variables from options
        self.dry_run = options['dry_run']
        self.debug = options['debug']
        self.force = options['force']
        
        if self.debug:
            logger.setLevel(logging.DEBUG)
        
        try:
            # Set up OpenAI API
            openai.api_key = settings.OPENAI_API_KEY
            
            # Get or create KHCC Brain instance and user
            khcc_brain = KHCCBrain.objects.first()
            if not khcc_brain:
                khcc_brain = KHCCBrain.objects.create()
                logger.info('Created new KHCC Brain instance')

            khcc_brain_user = KHCCBrain.get_user()
            
            # Use the custom lock implementation
            with cache_lock('khcc_brain_lock', timeout=3600) as acquired:
                if not acquired and not self.force:
                    self.stdout.write(
                        self.style.WARNING('Another KHCC Brain process is running. Use --force to override.')
                    )
                    return

                self.stdout.write("Starting KHCC Brain process...")

                # Join new teams
                teams_joined = self.ensure_team_memberships(khcc_brain_user)
                self.stdout.write(f"Joined {teams_joined} new teams")
                
                # Process projects
                projects_processed = self.handle_projects(
                    khcc_brain_user, 
                    last_hour
                )
                self.stdout.write(f"Processed {projects_processed} projects")
                
                # Process discussions
                discussions_processed = self.handle_discussions(
                    khcc_brain_user,
                    last_hour
                )
                self.stdout.write(f"Processed {discussions_processed} discussions")
                
                # Update brain statistics
                if not self.dry_run:
                    self.update_brain_stats(khcc_brain, khcc_brain_user)
            
            # Calculate runtime and metrics
            runtime = timezone.now() - start_time
            metrics = {
                'runtime_seconds': runtime.total_seconds(),
                'teams_joined': teams_joined,
                'projects_processed': projects_processed,
                'discussions_processed': discussions_processed,
                'total_comments': khcc_brain.total_comments,
                'dry_run': self.dry_run,
                'success': True
            }
            
            # Log metrics
            self.log_metrics(metrics)
            
            # Print success summary
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nKHCC Brain run completed successfully:"
                    f"\nRuntime: {runtime.total_seconds():.2f} seconds"
                    f"\nTeams joined: {teams_joined}"
                    f"\nProjects processed: {projects_processed}"
                    f"\nDiscussions processed: {discussions_processed}"
                    f"\nTotal comments: {khcc_brain.total_comments}"
                    f"\nDry run: {self.dry_run}"
                )
            )

            # Notify admins if significant activity occurred
            if not self.dry_run and (projects_processed + discussions_processed) > 10:
                admin_user = User.objects.filter(is_superuser=True).first()
                if admin_user:
                    Notification.objects.create(
                        recipient=admin_user,
                        sender=khcc_brain_user,
                        notification_type='system',
                        message=f"High activity detected: KHCC Brain processed {projects_processed} projects and {discussions_processed} discussions"
                    )

        except Exception as e:
            logger.error(f"Critical error in KHCC Brain execution: {str(e)}")
            self.log_metrics({
                'runtime_seconds': (timezone.now() - start_time).total_seconds(),
                'error': str(e),
                'success': False
            })
            raise