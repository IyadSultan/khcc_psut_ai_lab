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

    

    
    def should_respond_to_comment(self, comment, khcc_brain_user: Any, last_hour: timezone.datetime) -> bool:
        """Determine if KHCC Brain should respond to a specific comment"""
        # Get next comment in chain (if any)
        next_comment = Comment.objects.filter(
            project=comment.project,
            created_at__gt=comment.created_at
        ).order_by('created_at').first() if hasattr(comment, 'project') else TeamComment.objects.filter(
            discussion=comment.discussion,
            created_at__gt=comment.created_at
        ).order_by('created_at').first()

        # Don't respond if the next comment is from KHCC Brain
        if next_comment and next_comment.user == khcc_brain_user:
            return False

        # Check if this is a question or needs response
        needs_response = (
            '?' in comment.content or
            any(phrase in comment.content.lower() for phrase in [
                'how to', 'what about', 'can you', 'please', 'suggest',
                'help', 'advice', 'thoughts', 'opinion', 'next steps'
            ])
        )

        return needs_response

    def get_full_comment_chain(self, comment):
        """Get all comments in a chain including parent and replies"""
        comments = []
        
        # Get parent chain
        current = comment
        while current.parent:
            comments.append(current.parent)
            current = current.parent
        
        # Reverse parent chain to get chronological order
        comments.reverse()
        
        # Add the current comment
        comments.append(comment)
        
        # Get replies
        if hasattr(comment, 'replies'):
            replies = comment.replies.all().order_by('created_at')
            comments.extend(replies)
        
        return comments

    def check_needs_response(self, comment_chain, khcc_brain_user):
        """Check if a comment chain needs a response"""
        if not comment_chain:
            return False
            
        # Get last comment in chain
        last_comment = comment_chain[-1]
        
        # If last comment is from KHCC Brain, no response needed
        if (hasattr(last_comment, 'user') and last_comment.user == khcc_brain_user) or \
        (hasattr(last_comment, 'author') and last_comment.author == khcc_brain_user):
            return False
            
        # Check if it's a question or seems to need response
        needs_response = (
            '?' in last_comment.content or
            any(phrase in last_comment.content.lower() for phrase in [
                'how to', 'what about', 'can you', 'please', 'suggest',
                'help', 'advice', 'thoughts', 'opinion', 'next steps'
            ])
        )
        
        return needs_response

    def should_respond_to_project_comment(self, comment, khcc_brain_user: Any, last_hour: timezone.datetime) -> bool:
        """Check if KHCC Brain should respond to a project comment"""
        # For root comments
        if not comment.parent:
            # Check if any reply from brain exists
            brain_replied = Comment.objects.filter(
                project=comment.project,
                user=khcc_brain_user,
                parent=comment
            ).exists()
            return not brain_replied

        # For reply comments
        # Get the root comment
        root_comment = comment
        while root_comment.parent:
            root_comment = root_comment.parent

        # Get all replies after this comment
        later_replies = Comment.objects.filter(
            project=comment.project,
            created_at__gt=comment.created_at,
            parent=root_comment
        )

        # Check if brain has replied after this comment
        brain_replied = any(reply.user == khcc_brain_user for reply in later_replies)
        
        return not brain_replied

    def should_respond_to_team_comment(self, comment, khcc_brain_user: Any, last_hour: timezone.datetime) -> bool:
        """Check if KHCC Brain should respond to a team comment"""
        # Get all later comments in the same discussion
        later_comments = TeamComment.objects.filter(
            discussion=comment.discussion,
            created_at__gt=comment.created_at
        )

        # Check if brain has commented after this comment
        brain_commented = later_comments.filter(author=khcc_brain_user).exists()
        
        return not brain_commented

    def handle_projects(self, khcc_brain_user: Any, last_hour: timezone.datetime) -> int:
        """Process projects and their comments"""
        try:
            logger.info("Starting project comment processing...")
            
            # Get both recent comments and older unanswered comments
            comments_to_check = Comment.objects.filter(
                Q(created_at__gte=last_hour) |  # Recent comments
                ~Q(project__comments__user=khcc_brain_user) |  # Projects with no brain comments
                Q(project__comments__user=khcc_brain_user, 
                project__comments__created_at__lt=F('created_at'))  # Comments after brain's last response
            ).exclude(
                user=khcc_brain_user
            ).select_related('project', 'user', 'parent').distinct().order_by('created_at')
            
            logger.info(f"Found {comments_to_check.count()} comments to check")
            
            processed_count = 0
            for comment in comments_to_check:
                # Check if brain has already responded to this comment
                brain_response = Comment.objects.filter(
                    project=comment.project,
                    user=khcc_brain_user,
                    created_at__gt=comment.created_at,
                    parent=comment if not comment.parent else comment.parent
                ).exists()
                
                if not brain_response:
                    logger.info(f"Processing comment by {comment.user.username} in project '{comment.project.title}'")
                    logger.info(f"Comment content: {comment.content[:100]}...")
                    
                    feedback = self.analyze_comment_chain(comment, khcc_brain_user)
                    
                    if feedback and not self.dry_run:
                        # Create response as a reply to the appropriate comment
                        new_comment = Comment.objects.create(
                            project=comment.project,
                            user=khcc_brain_user,
                            content=feedback,
                            parent=comment if not comment.parent else comment.parent
                        )
                        
                        # Notify the comment author
                        Notification.objects.create(
                            recipient=comment.user,
                            sender=khcc_brain_user,
                            notification_type='comment',
                            project=comment.project,
                            message=f"KHCC Brain responded to your comment"
                        )
                        
                        processed_count += 1
                        logger.info(f"Added response to comment")
                        time.sleep(self.rate_limit_delay)

            return processed_count

        except Exception as e:
            logger.error(f"Error processing projects: {str(e)}")
            return 0

    def handle_discussions(self, khcc_brain_user: Any, last_hour: timezone.datetime) -> int:
        """Process team discussions and comments"""
        try:
            logger.info("Starting discussion comment processing...")
            
            # Get both recent comments and older unanswered comments
            comments_to_check = TeamComment.objects.filter(
                Q(created_at__gte=last_hour) |  # Recent comments
                ~Q(discussion__comments__author=khcc_brain_user) |  # Discussions with no brain comments
                Q(discussion__comments__author=khcc_brain_user,
                discussion__comments__created_at__lt=F('created_at'))  # Comments after brain's last response
            ).exclude(
                author=khcc_brain_user
            ).select_related('discussion', 'author', 'discussion__team').distinct().order_by('created_at')
            
            logger.info(f"Found {comments_to_check.count()} discussion comments to check")
            
            processed_count = 0
            for comment in comments_to_check:
                # Check if brain has already responded to this comment thread
                brain_response = TeamComment.objects.filter(
                    discussion=comment.discussion,
                    author=khcc_brain_user,
                    created_at__gt=comment.created_at
                ).exists()
                
                if not brain_response:
                    logger.info(f"Processing comment by {comment.author.username} in discussion '{comment.discussion.title}'")
                    logger.info(f"Comment content: {comment.content[:100]}...")
                    
                    feedback = self.analyze_comment_chain(comment, khcc_brain_user)
                    
                    if feedback and not self.dry_run:
                        # Create response
                        new_comment = TeamComment.objects.create(
                            discussion=comment.discussion,
                            author=khcc_brain_user,
                            content=feedback
                        )
                        
                        # Notify team members
                        team_members = comment.discussion.team.memberships.filter(
                            is_approved=True,
                            receive_notifications=True
                        ).exclude(user=khcc_brain_user)

                        if team_members.exists():
                            Notification.objects.bulk_create([
                                Notification(
                                    recipient=member.user,
                                    sender=khcc_brain_user,
                                    notification_type='comment',
                                    message=f"KHCC Brain responded to a comment in discussion: {comment.discussion.title}"
                                ) for member in team_members
                            ])
                        
                        processed_count += 1
                        logger.info(f"Added response to discussion comment")
                        time.sleep(self.rate_limit_delay)

            return processed_count

        except Exception as e:
            logger.error(f"Error processing discussions: {str(e)}")
            return 0

    def analyze_comment_chain(self, comment, khcc_brain_user: Any) -> Optional[str]:
        """Generate response to a comment chain"""
        try:
            # Get full comment chain context
            if hasattr(comment, 'project'):
                chain = self.get_full_comment_chain(comment)
                context_obj = comment.project
                context_type = "project"
                author_field = 'user'
            else:
                chain = self.get_full_comment_chain(comment)  # For consistency
                context_obj = comment.discussion
                context_type = "discussion"
                author_field = 'author'

            # Build conversation history with clear structure
            conversation_text = ""
            for idx, c in enumerate(chain, 1):
                author = getattr(c, author_field).username
                indent = "    " * (c.parent.id if hasattr(c, 'parent') and c.parent else 0)
                conversation_text += f"{indent}{idx}. {author}: {c.content}\n"

            prompt = f"""
            As KHCC Brain, respond to this comment chain in a healthcare {context_type}.

            {context_type.title()}: {context_obj.title}
            
            Full Conversation:
            {conversation_text}

            Latest Comment by {getattr(comment, author_field).username}:
            {comment.content}

            Provide a response that:
            1. Addresses the latest comment directly
            2. References relevant points from the conversation history
            3. Maintains context of the full discussion
            4. Offers healthcare-specific insights
            5. Encourages further productive discussion

            If this is a question or request:
            - Provide clear, actionable answers
            - Reference previous context where relevant
            - Suggest related considerations
            - Offer specific examples or steps

            Format using Markdown with:
            - Clear section headings
            - Bullet points for key ideas
            - Healthcare-focused recommendations
            
            Keep response under 200 words and maintain healthcare focus.
            End with "Best regards, KHCC Brain 🤖"
            """

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are KHCC Brain, an AI healthcare research assistant. Provide helpful, specific responses focused on healthcare and medical applications."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error analyzing comment chain: {str(e)}")
            return self.get_fallback_response('comment')

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

                        # Create welcome discussion - no need for URL reversing
                        discussion = TeamDiscussion.objects.create(
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
                        continue

            return joined_count

        except Exception as e:
            logger.error(f"Error ensuring team memberships: {str(e)}")
            return 0
    
    def handle_discussions(self, khcc_brain_user: Any, last_hour: timezone.datetime) -> int:
        """Process team discussions"""
        try:
            # Get active discussions excluding those where KHCC Brain already commented recently
            active_discussions = TeamDiscussion.objects.filter(
                Q(created_at__gte=last_hour) |  # New discussions
                Q(comments__created_at__gte=last_hour)  # Discussions with recent comments
            ).exclude(
                # Exclude discussions where KHCC Brain commented after the last activity
                comments__author=khcc_brain_user,
                comments__created_at__gt=F('comments__created_at')
            ).distinct()

            processed_count = 0
            skipped_count = 0

            for discussion in active_discussions:
                try:
                    # Get all comments for this discussion
                    discussion_comments = TeamComment.objects.filter(
                        discussion=discussion
                    ).order_by('created_at')
                    
                    # Get KHCC Brain's last comment if any
                    last_brain_comment = discussion_comments.filter(
                        author=khcc_brain_user
                    ).order_by('-created_at').first()

                    # Get latest non-brain comment
                    last_other_comment = discussion_comments.exclude(
                        author=khcc_brain_user
                    ).order_by('-created_at').first()

                    should_comment = (
                        not last_brain_comment or  # Never commented before
                        (last_other_comment and  # There's a new comment from someone else
                        (not last_brain_comment or last_other_comment.created_at > last_brain_comment.created_at))
                    )

                    if should_comment:
                        logger.info(f"Processing discussion: {discussion.title} (ID: {discussion.id})")
                        
                        feedback = self.analyze_discussion(discussion, khcc_brain_user)
                        if feedback and not self.dry_run:
                            try:
                                # Create the comment
                                comment = TeamComment.objects.create(
                                    discussion=discussion,
                                    author=khcc_brain_user,
                                    content=feedback
                                )

                                # Only notify team members who have notifications enabled
                                team_members = TeamMembership.objects.filter(
                                    team=discussion.team,
                                    is_approved=True,
                                    receive_notifications=True
                                ).exclude(user=khcc_brain_user)

                                # Create notifications
                                notifications = [
                                    Notification(
                                        recipient=member.user,
                                        sender=khcc_brain_user,
                                        notification_type='comment',
                                        message=f"KHCC Brain commented on discussion: {discussion.title}"
                                    )
                                    for member in team_members
                                ]

                                # Bulk create notifications
                                if notifications:
                                    Notification.objects.bulk_create(notifications)

                                processed_count += 1
                                time.sleep(self.rate_limit_delay)
                                
                                logger.info(f"Successfully commented on discussion: {discussion.title}")
                            except Exception as comment_error:
                                logger.error(f"Error creating comment for discussion {discussion.id}: {str(comment_error)}")
                    else:
                        skipped_count += 1
                        logger.debug(f"Skipped discussion: {discussion.title} (already processed)")

                except Exception as disc_error:
                    logger.error(f"Error processing discussion {discussion.id}: {str(disc_error)}")
                    continue

            logger.info(f"Processed {processed_count} discussions, skipped {skipped_count}")
            return processed_count

        except Exception as e:
            logger.error(f"Error in handle_discussions: {str(e)}")
            return 0

    def analyze_discussion(self, discussion: TeamDiscussion, khcc_brain_user: Any) -> Optional[str]:
        """Generate AI-powered analysis of team discussion"""
        try:
            cache_key = f"khcc_brain_discussion_{discussion.id}_{discussion.updated_at.isoformat()}"
            cached_response = self.get_cached_response(cache_key)
            if cached_response:
                return cached_response

            if not self.check_rate_limit('discussion_analysis'):
                return None

            # Get all comments for context
            comments = TeamComment.objects.filter(
                discussion=discussion
            ).order_by('created_at').select_related('author')

            # Create discussion history text
            comments_text = "\n".join([
                f"{comment.author.username} ({comment.created_at.strftime('%Y-%m-%d %H:%M')}): {comment.content}"
                for comment in comments
            ])

            # Get team context
            team_members = discussion.team.memberships.filter(is_approved=True).count()
            team_discussions = discussion.team.discussions.count()

            prompt = f"""
            As KHCC Brain, analyze this healthcare team discussion and provide constructive input.

            Team: {discussion.team.name} ({team_members} members, {team_discussions} total discussions)
            Discussion Title: {discussion.title}
            Initial Post: {discussion.content}
            Discussion History:
            {comments_text}

            Provide feedback that:
            1. Synthesizes key points from all comments
            2. Relates topics to healthcare applications
            3. Suggests potential collaboration points
            4. Proposes specific next steps
            5. Encourages team participation

            Format using Markdown:
            - Use ## for main sections
            - Bullet points for key insights
            - Healthcare-specific recommendations
            - Technical suggestions if relevant
            - References to team members' inputs where appropriate

            Keep response under 200 words and healthcare-focused.
            End with "Best regards, KHCC Brain 🤖"
            """

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are KHCC Brain, an AI healthcare research mentor focused on fostering team collaboration in medical research. Your responses should be constructive, specific to healthcare, and focused on advancing the team's goals."
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
            logger.error(f"Error analyzing discussion {discussion.id}: {str(e)}")
            return self.get_fallback_response('discussion')
        
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

                logger.info("Starting KHCC Brain process...")

                # Join new teams
                teams_joined = self.ensure_team_memberships(khcc_brain_user)
                self.stdout.write(f"Joined {teams_joined} new teams")

                # Get active items count before processing
                active_projects = Project.objects.filter(
                    Q(comments__created_at__gte=last_hour) |
                    Q(created_at__gte=last_hour)
                ).distinct().count()
                
                active_discussions = TeamDiscussion.objects.filter(
                    Q(comments__created_at__gte=last_hour) |
                    Q(created_at__gte=last_hour)
                ).distinct().count()
                
                logger.info(f"Found {active_projects} active projects and {active_discussions} active discussions")
                
                # Process items
                projects_processed = self.handle_projects(khcc_brain_user, last_hour)
                discussions_processed = self.handle_discussions(khcc_brain_user, last_hour)
                
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