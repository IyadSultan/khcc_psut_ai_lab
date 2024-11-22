# projects/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import timedelta
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.db.models import Avg
from django.conf import settings
from khcc_psut_ai_lab.constants import TALENT_TYPES
from django.utils import timezone
import openai
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .services import OpenAITaggingService


            
# Add these constants
gold_goalS = [
    ('all', 'All Complete'),
    ('first', 'First to Complete'),
    ('best', 'Best Solution')
]

# File Upload Path Functions
def validate_github_url(value):
    if not value.startswith(('https://github.com/', 'http://github.com/')):
        raise ValidationError('URL must be a GitHub repository')

def project_file_upload_path(instance, filename):
    """Generate upload path for project files"""
    return f'uploads/user_{instance.author.id}/project_{instance.pk}/{filename}'

def project_image_upload_path(instance, filename):
    """Generate upload path for project images"""
    return f'images/projects/user_{instance.author.id}/{filename}'

def avatar_upload_path(instance, filename):
    """Generate upload path for user avatars"""
    return f'avatars/user_{instance.user.id}/{filename}'

def comment_image_upload_path(instance, filename):
    """Generate upload path for comment images"""
    return f'images/comments/user_{instance.user.id}/{filename}'

# Add to models.py
from urllib.parse import urlparse, parse_qs

def validate_youtube_url(url):
    if not url:
        return
    
    try:
        parsed = urlparse(url)
        if parsed.hostname not in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            raise ValidationError('Only YouTube URLs are allowed')
            
        if parsed.hostname in ['youtube.com', 'www.youtube.com']:
            if not parsed.path.startswith('/watch'):
                raise ValidationError('Invalid YouTube URL format')
            if not parse_qs(parsed.query).get('v'):
                raise ValidationError('Invalid YouTube URL format')
        elif parsed.hostname == 'youtu.be':
            if not parsed.path[1:]:
                raise ValidationError('Invalid YouTube URL format')
    except Exception:
        raise ValidationError('Invalid YouTube URL')
    
class VirtualMember(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='virtual_members/')
    specialty = models.CharField(max_length=100)
    description = models.TextField()
    projects = models.ManyToManyField('Project', related_name='virtual_team_members')

    def __str__(self):
        return self.name

class Startup(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='startup_logos/')
    description = models.TextField()
    website = models.URLField()
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField('Product', related_name='startups')    
# Models
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    description = models.TextField()
    github_link = models.URLField(validators=[URLValidator(), validate_github_url], blank=True, null=True)
    tags = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Enter tags separated by commas"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    clap_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    virtual_members = models.ManyToManyField(VirtualMember, related_name='assigned_projects')
    generated_tags = models.TextField(blank=True)  # AI-generated tags
    
    # File fields
    pdf_file = models.FileField(
        upload_to=project_file_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True,
        blank=True,
        help_text="Upload a PDF document (max 10MB)"
    )
    
    featured_image = models.ImageField(
        upload_to=project_image_upload_path,
        null=True,
        blank=True,
        help_text="Upload a featured image for your project"
    )
    
    additional_files = models.FileField(
        upload_to=project_file_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'zip']
            )
        ],
        null=True,
        blank=True,
        help_text="Upload additional files (PDF, DOC, TXT, ZIP - max 10MB)"
    )
    
    rating_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)

    youtube_url = models.URLField(
        validators=[validate_youtube_url],
        blank=True,
        null=True,
        help_text="Link to a YouTube video for your project"
    )
    
    # New fields for Gold Seeds
    is_gold = models.BooleanField(default=False, help_text="Mark this as a Gold Seed (Faculty only)")
    token_reward = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Number of tokens awarded for completion"
    )
    gold_goal = models.CharField(
        max_length=10,
        choices=gold_goalS,
        null=True,
        blank=True
    )
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def get_youtube_embed_url(self):
        """Convert YouTube video URL to embed URL"""
        if not self.youtube_url:
            return None
            
        video_id = None
        parsed = urlparse(self.youtube_url)
        
        if 'youtube.com' in parsed.hostname:
            query = parse_qs(parsed.query)
            video_id = query.get('v', [None])[0]
        elif 'youtu.be' in parsed.hostname:
            video_id = parsed.path.lstrip('/')
            
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate base slug from title
            base_slug = slugify(self.title)
            
            # Check if the base slug exists
            if Project.objects.filter(slug=base_slug).exists():
                # If it exists, append a UUID to make it unique
                base_slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
            
            self.slug = base_slug
            
        super().save(*args, **kwargs)
    


    @property
    def comment_count(self):
        """Get total number of comments"""
        return self.comments.count()
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def user_has_clapped(self, user):
        return self.claps.filter(user=user).exists()
    
    @property
    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return round(float(self.rating_total) / self.rating_count, 1)

    
    def generate_zip(self):
        """Generate a ZIP file of the project"""
        zip_filename = f"{self.slug}_project.zip"
        zip_path = os.path.join(settings.MEDIA_ROOT, 'project_zips', zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            if self.pdf_file:
                zip_file.write(self.pdf_file.path, os.path.basename(self.pdf_file.name))
            if self.additional_files:
                zip_file.write(self.additional_files.path, os.path.basename(self.additional_files.name))
            
            # Add README with project info
            readme_content = f"""
            Project: {self.title}
            Author: {self.author.username}
            Description: {self.description}
            Tags: {self.tags}
            Created: {self.created_at}
            """
            zip_file.writestr('README.txt', readme_content)
        
        return zip_path
    
    
    def clean(self):
        super().clean()
        # Validate file sizes
        if self.pdf_file and self.pdf_file.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError({'pdf_file': 'PDF file must be smaller than 10MB'})
        if self.additional_files and self.additional_files.size > 10 * 1024 * 1024:
            raise ValidationError({'additional_files': 'File must be smaller than 10MB'})
        if self.featured_image and self.featured_image.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError({'featured_image': 'Image must be smaller than 5MB'})

    def update_rating_stats(self):
        """Update the rating statistics"""
        ratings = self.ratings.all()
        count = ratings.count()
        if count > 0:
            total = sum(r.score for r in ratings)
            self.rating_total = total
            self.rating_count = count
        else:
            self.rating_total = 0
            self.rating_count = 0
        self.save()

    def get_featured_image_url(self):
        """Get the featured image URL or return None"""
        return self.featured_image.url if self.featured_image else None
        
    def get_pdf_url(self):
        """Get the PDF file URL or return None"""
        return self.pdf_file.url if self.pdf_file else None

    def can_submit(self):
        if not self.is_gold or not self.deadline:
            return False
        return timezone.now() <= self.deadline

class Application(models.Model):
    APPLICATION_TYPES = [
        ('sponsor', 'Sponsor'),
        ('team', 'Team Member'),
    ]
    
    LEVEL_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]

    type = models.CharField(max_length=20, choices=APPLICATION_TYPES)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    organization = models.CharField(max_length=200, blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True, null=True)
    message = models.TextField(help_text="Tell us about yourself or your organization")
    attachment = models.FileField(
        upload_to='applications/',
        help_text="PDF format preferred, max 10MB",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"

class Comment(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField(
        upload_to=comment_image_upload_path,
        null=True,
        blank=True,
        help_text="Upload an image (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    clap_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['created_at']
    
    def user_has_clapped(self, user):
        return self.claps.filter(user=user).exists()
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.title}'


    
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    github_username = models.CharField(max_length=39, blank=True) 
    linkedin_url = models.URLField(blank=True)
    twitter_username = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    research_interests = models.TextField(blank=True)
    talent_type = models.CharField(
        max_length=20,
        choices=TALENT_TYPES,
        default='ai',
        verbose_name='Talent Type'
    )
    
    
    @property
    def is_faculty(self):
        return self.user.groups.filter(name='Faculty').exists()
    
    # Notification settings
    email_on_comment = models.BooleanField(default=True)
    email_on_follow = models.BooleanField(default=True)
    email_on_clap = models.BooleanField(default=False)
    email_on_bookmark = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_talent_display(self):
        return dict(TALENT_TYPES).get(self.talent_type, '')

class Clap(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='claps', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='user_claps', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('project', 'user')
    
    def __str__(self):
        return f'{self.user.username} clapped for {self.project.title}'

class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    )
    
    project = models.ForeignKey(
        Project, 
        related_name='ratings', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('project', 'user')
        
    def __str__(self):
        return f"{self.user.username}'s {self.score}-star rating on {self.project.title}"

class Bookmark(models.Model):
    user = models.ForeignKey(
        User, 
        related_name='bookmarks', 
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project, 
        related_name='bookmarks', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('user', 'project')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.project.title}"

class ProjectAnalytics(models.Model):
    project = models.OneToOneField(
        Project, 
        on_delete=models.CASCADE, 
        related_name='analytics'
    )
    view_count = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    github_clicks = models.PositiveIntegerField(default=0)
    avg_time_spent = models.DurationField(default=timedelta)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Traffic sources
    direct_traffic = models.PositiveIntegerField(default=0)
    social_traffic = models.PositiveIntegerField(default=0)
    search_traffic = models.PositiveIntegerField(default=0)
    referral_traffic = models.PositiveIntegerField(default=0)
    
    # Device stats
    desktop_visits = models.PositiveIntegerField(default=0)
    mobile_visits = models.PositiveIntegerField(default=0)
    tablet_visits = models.PositiveIntegerField(default=0)
    
    # Browser stats
    chrome_visits = models.PositiveIntegerField(default=0)
    firefox_visits = models.PositiveIntegerField(default=0)
    safari_visits = models.PositiveIntegerField(default=0)
    edge_visits = models.PositiveIntegerField(default=0)
    other_browsers = models.PositiveIntegerField(default=0)
    
    # Weekly and monthly stats
    unique_visitors_weekly = models.PositiveIntegerField(default=0)
    unique_visitors_monthly = models.PositiveIntegerField(default=0)
    github_clicks_weekly = models.PositiveIntegerField(default=0)
    github_clicks_monthly = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Project analytics"
        
    def __str__(self):
        return f"Analytics for {self.project.title}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('clap', 'Clap'),
        ('bookmark', 'Bookmark'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Notification for {self.recipient.username}'

    @classmethod
    def create(cls, recipient, sender, notification_type, project=None, message=None):
        if not message:
            message = cls.get_default_message(notification_type, sender, project)
        return cls.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            project=project,
            message=message
        )

    @staticmethod
    def get_default_message(notification_type, sender, project=None):
        username = sender.username
        if project:
            project_title = project.title
            if notification_type == 'clap':
                return f"{username} clapped for your project '{project_title}'"
            elif notification_type == 'comment':
                return f"{username} commented on your project '{project_title}'"
            elif notification_type == 'rating':
                return f"{username} rated your project '{project_title}'"
            elif notification_type == 'bookmark':
                return f"{username} bookmarked your project '{project_title}'"
        elif notification_type == 'follow':
            return f"{username} started following you"
        return "You have a new notification"

class Follow(models.Model):
    follower = models.ForeignKey(
        User, 
        related_name='following',  # User.following.all() gets all users this user follows
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, 
        related_name='followers',  # User.followers.all() gets all users following this user
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class CommentClap(models.Model):
    comment = models.ForeignKey(Comment, related_name='claps', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_claps', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.user.username} clapped for comment on {self.comment.project.title}'
    

class Solution(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='solutions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    files = models.FileField(
        upload_to='solutions/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'zip', 'py', 'ipynb', 'txt']
        )]
    )
    github_link = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    faculty_feedback = models.TextField(blank=True)
    tokens_awarded = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['project', 'user']

    def __str__(self):
        return f"Solution by {self.user.username} for {self.project.title}"



from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from khcc_psut_ai_lab.constants import DEFAULT_TEAM_SIZE, MAX_TEAM_SIZE, TEAM_ROLES
import uuid

def team_image_upload_path(instance, filename):
    # Generate path like: team_images/team_slug/filename
    return f'team_images/{instance.slug}/{filename}'

class Team(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    description = models.TextField()
    founder = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='founded_teams'
    )
    team_image = models.ImageField(  # Changed from 'image' to 'team_image'
        upload_to=team_image_upload_path,
        null=True,
        blank=True,
        help_text="Upload a team profile image"
    )
    tags = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Enter tags separated by commas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        TeamAnalytics.objects.get_or_create(team=self)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class TeamMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('founder', 'Founder'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    receive_notifications = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['team', 'user']

class TeamDiscussion(models.Model):
    """Model for team discussion threads"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pinned = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-pinned', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.team.name}"

class TeamComment(models.Model):
    """Model for comments on team discussions"""
    discussion = models.ForeignKey(TeamDiscussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.discussion.title}"



class TeamAnalytics(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='analytics')
    total_discussions = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    active_members = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    # Weekly and monthly stats
    discussions_this_week = models.PositiveIntegerField(default=0)
    comments_this_week = models.PositiveIntegerField(default=0)
    discussions_this_month = models.PositiveIntegerField(default=0)
    comments_this_month = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Team analytics"

    def __str__(self):
        return f"Analytics for {self.team.name}"

    def update_stats(self):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        self.total_discussions = self.team.discussions.count()
        self.total_comments = TeamComment.objects.filter(discussion__team=self.team).count()
        self.active_members = TeamMembership.objects.filter(
            team=self.team,
            user__last_login__gte=month_ago
        ).count()
        
        self.discussions_this_week = self.team.discussions.filter(
            created_at__gte=week_ago
        ).count()
        self.comments_this_week = TeamComment.objects.filter(
            discussion__team=self.team,
            created_at__gte=week_ago
        ).count()
        
        self.discussions_this_month = self.team.discussions.filter(
            created_at__gte=month_ago
        ).count()
        self.comments_this_month = TeamComment.objects.filter(
            discussion__team=self.team,
            created_at__gte=month_ago
        ).count()
        
        self.last_activity = now
        self.save()


class Sponsorship(models.Model):
    LEVELS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum')
    ]
    
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsor_logos/')
    level = models.CharField(max_length=20, choices=LEVELS)
    website = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

class Tool(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='tool_images/')
    url = models.URLField()
    github_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Dataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='datasets/')
    size = models.BigIntegerField()  # in bytes
    format = models.CharField(max_length=50)
    license = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    downloads = models.IntegerField(default=0)

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

# In your models.py, add the imports at the top
from django.conf import settings
import openai

# Add this class to your existing models.py, at the end of the file
class KHCCBrain(models.Model):
    """AI Research Assistant Model"""
    name = models.CharField(default="KHCC Brain", max_length=50)
    description = models.CharField(default="AI Research Assistant & Team Mentor", max_length=100)
    last_active = models.DateTimeField(auto_now=True)
    total_comments = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "KHCC Brain"
        verbose_name_plural = "KHCC Brain Instances"

    def analyze_project(self, project):
        """Analyze a project and generate insights using OpenAI"""
        try:
            # Set OpenAI API key
            openai.api_key = settings.OPENAI_API_KEY
            
            # Get latest comments
            latest_comments = project.comments.order_by('-created_at')[:5]
            comments_text = "\n".join([f"- {comment.content}" for comment in latest_comments])
            
            prompt = f"""
            You are KHCC Brain, an AI research assistant at KHCC AI Lab. Analyze this project and provide encouraging feedback.
            Be constructive, specific, and mention both strengths and potential next steps.
            Use a friendly, encouraging tone with a focus on healthcare and AI applications.

            Project Title: {project.title}
            Description: {project.description}
            Recent Comments:
            {comments_text}
            
            Generate concise feedback focusing on:
            1. Specific achievements and potential in healthcare AI
            2. Response to recent discussions and comments
            3. Suggestions for next steps and research directions
            4. Team collaboration opportunities
            
            Keep your response encouraging and under 200 words.
            """

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are KHCC Brain, a helpful AI research assistant focusing on healthcare and AI projects."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating AI feedback: {str(e)}")
            return "I'm currently experiencing some technical difficulties, but I'll analyze this project as soon as possible!"

    def analyze_team_discussion(self, discussion):
        """Analyze team discussion and provide strategic advice"""
        try:
            openai.api_key = settings.OPENAI_API_KEY
            
            # Get all comments in the discussion
            comments = discussion.comments.order_by('created_at')
            comments_text = "\n".join([
                f"- {comment.author.username}: {comment.content}" 
                for comment in comments
            ])
            
            prompt = f"""
            As KHCC Brain, analyze this team discussion and provide constructive input.
            
            Discussion Title: {discussion.title}
            Initial Post: {discussion.content}
            
            Discussion History:
            {comments_text}
            
            Provide concise feedback that:
            1. Acknowledges key points raised in the discussion
            2. Offers relevant healthcare AI insights
            3. Suggests potential collaboration opportunities
            4. Proposes concrete next steps
            
            Keep your response encouraging and under 150 words.
            Your tone should be professional but friendly.
            """

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are KHCC Brain, a healthcare AI research mentor focused on fostering collaboration."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating team feedback: {str(e)}")
            return "I'm currently experiencing some technical difficulties, but I'll join the discussion as soon as possible!"

    @classmethod
    def get_user(cls):
        """Get or create the KHCC Brain user account"""
        try:
            return User.objects.get(username='khcc_brain')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='khcc_brain',
                email='khcc_brain@khcc.jo',
                first_name='KHCC',
                last_name='Brain',
                is_active=True
            )
            
            # Create profile
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': "I am KHCC Brain, an AI research assistant specializing in healthcare AI. I help teams advance their medical AI projects through analysis and suggestions.",
                    'title': "AI Research Assistant",
                    'department': "AI Lab",
                    'talent_type': 'ai'
                }
            )
            return user