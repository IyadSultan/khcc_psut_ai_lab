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

# Models
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    github_link = models.URLField(validators=[URLValidator(), validate_github_url])
    tags = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Enter tags separated by commas"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    claps = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Create upload directory if it doesn't exist
        if not self.pk:  # Only for new instances
            super().save(*args, **kwargs)
            upload_dir = os.path.dirname(project_file_upload_path(self, ''))
            os.makedirs(os.path.join('media', upload_dir), exist_ok=True)
        else:
            super().save(*args, **kwargs)
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    @property
    def comment_count(self):
        return self.comments.count()
        
    def user_has_clapped(self, user):
        return self.claps_set.filter(user=user).exists()
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return None
        return sum(r.score for r in ratings) / len(ratings)

    def clean(self):
        super().clean()
        # Validate file sizes
        if self.pdf_file and self.pdf_file.size > 10 * 1024 * 1024:  # 10MB
            raise ValidationError({'pdf_file': 'PDF file must be smaller than 10MB'})
        if self.additional_files and self.additional_files.size > 10 * 1024 * 1024:
            raise ValidationError({'additional_files': 'File must be smaller than 10MB'})
        if self.featured_image and self.featured_image.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError({'featured_image': 'Image must be smaller than 5MB'})

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
    
    class Meta:
        ordering = ['created_at']
    
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
    
    # Notification settings
    email_on_comment = models.BooleanField(default=True)
    email_on_follow = models.BooleanField(default=True)
    email_on_clap = models.BooleanField(default=False)
    email_on_bookmark = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Clap(models.Model):
    project = models.ForeignKey(
        Project, 
        related_name='claps_set', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

