# Combined Python and HTML files
# Generated from directory: C:\Users\isultan\Documents\khcc_psut_ai_lab\khcc_psut_ai_lab\projects
# Total files found: 27



# Contents from: .\__init__.py


# Contents from: .\admin.py
# projects/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.utils.safestring import mark_safe
from .models import (
    Project, Comment, Clap, UserProfile, Rating,
    Bookmark, ProjectAnalytics, Notification
)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author_link', 'created_at', 'claps_count',
        'comments_count', 'ratings_count', 'github_link_display'
    ]
    list_filter = ['created_at', 'author', 'tags']
    search_fields = ['title', 'description', 'author__username', 'tags']
    readonly_fields = ['created_at', 'updated_at', 'slug', 'claps']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'github_link', 'tags')
        }),
        ('Author Information', {
            'fields': ('author',)
        }),
        ('Metrics', {
            'fields': ('claps',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def author_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)
    author_link.short_description = 'Author'
    
    def claps_count(self, obj):
        return obj.claps
    claps_count.short_description = 'Claps'
    
    def comments_count(self, obj):
        count = obj.comments.count()
        url = reverse('admin:projects_comment_changelist')
        return format_html('<a href="{}?project__id={}">{}</a>', url, obj.id, count)
    comments_count.short_description = 'Comments'
    
    def ratings_count(self, obj):
        count = obj.ratings.count()
        url = reverse('admin:projects_rating_changelist')
        return format_html('<a href="{}?project__id={}">{}</a>', url, obj.id, count)
    ratings_count.short_description = 'Ratings'
    
    def github_link_display(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', 
                         obj.github_link, obj.github_link)
    github_link_display.short_description = 'GitHub Repository'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'project_link', 'parent_comment',
        'created_at', 'content_preview', 'has_replies'
    ]
    list_filter = ['created_at', 'user', 'project']
    search_fields = ['content', 'user__username', 'project__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def project_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.title)
    project_link.short_description = 'Project'
    
    def parent_comment(self, obj):
        if obj.parent:
            return format_html('Reply to: {}', obj.parent.content[:50])
        return '-'
    parent_comment.short_description = 'Parent Comment'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
    
    def has_replies(self, obj):
        count = obj.replies.count()
        if count:
            url = reverse('admin:projects_comment_changelist')
            return format_html('<a href="{}?parent__id={}">{} replies</a>', 
                             url, obj.id, count)
        return 'No replies'
    has_replies.short_description = 'Replies'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_link', 'location', 'github_username',
        'project_count', 'total_claps_received', 'avatar_preview'
    ]
    list_filter = ['location', 'created_at']
    search_fields = ['user__username', 'bio', 'location', 'github_username']
    readonly_fields = [
        'created_at', 'updated_at', 'avatar_preview',
        'project_count', 'total_claps_received'
    ]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar', 'avatar_preview', 'bio')
        }),
        ('Contact Information', {
            'fields': ('location', 'website')
        }),
        ('Social Links', {
            'fields': ('github_username', 'linkedin_url')
        }),
        ('Statistics', {
            'fields': ('project_count', 'total_claps_received'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.avatar.url
            )
        return 'No avatar'
    avatar_preview.short_description = 'Avatar Preview'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'recipient_link', 'sender_link', 'notification_type',
        'is_read', 'created_at', 'message_preview'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = [
        'recipient__username', 'sender__username',
        'message', 'project__title'
    ]
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def recipient_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.recipient.id])
        return format_html('<a href="{}">{}</a>', url, obj.recipient.username)
    recipient_link.short_description = 'Recipient'
    
    def sender_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.sender.id])
        return format_html('<a href="{}">{}</a>', url, obj.sender.username)
    sender_link.short_description = 'Sender'
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected notifications as unread"

@admin.register(ProjectAnalytics)
class ProjectAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'project_link', 'view_count', 'unique_visitors',
        'github_clicks', 'last_updated'
    ]
    list_filter = ['last_updated']
    readonly_fields = [
        'view_count', 'unique_visitors', 'github_clicks',
        'avg_time_spent', 'direct_traffic', 'social_traffic',
        'search_traffic', 'referral_traffic', 'desktop_visits',
        'mobile_visits', 'tablet_visits', 'chrome_visits',
        'firefox_visits', 'safari_visits', 'edge_visits',
        'other_browsers', 'unique_visitors_weekly',
        'unique_visitors_monthly', 'github_clicks_weekly',
        'github_clicks_monthly', 'last_updated'
    ]
    
    fieldsets = (
        ('Project Information', {
            'fields': ('project',)
        }),
        ('Basic Metrics', {
            'fields': (
                'view_count', 'unique_visitors',
                'github_clicks', 'avg_time_spent'
            )
        }),
        ('Traffic Sources', {
            'fields': (
                'direct_traffic', 'social_traffic',
                'search_traffic', 'referral_traffic'
            ),
            'classes': ('collapse',)
        }),
        ('Device Statistics', {
            'fields': (
                'desktop_visits', 'mobile_visits',
                'tablet_visits'
            ),
            'classes': ('collapse',)
        }),
        ('Browser Statistics', {
            'fields': (
                'chrome_visits', 'firefox_visits',
                'safari_visits', 'edge_visits',
                'other_browsers'
            ),
            'classes': ('collapse',)
        }),
        ('Time-based Metrics', {
            'fields': (
                'unique_visitors_weekly',
                'unique_visitors_monthly',
                'github_clicks_weekly',
                'github_clicks_monthly'
            ),
            'classes': ('collapse',)
        })
    )
    
    def project_link(self, obj):
        url = reverse('admin:projects_project_change', args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', url, obj.project.title)
    project_link.short_description = 'Project'

class CustomAdminSite(admin.AdminSite):
    site_header = 'KHCC AI Lab Administration'
    site_title = 'KHCC AI Lab Admin'
    index_title = 'Dashboard'
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Add custom statistics to the admin index
        app_list.append({
            'name': 'Statistics',
            'app_label': 'statistics',
            'models': [
                {
                    'name': 'Total Seeds',
                    'object_name': 'projects',
                    'count': Project.objects.count(),
                    'admin_url': reverse('admin:projects_project_changelist'),
                },
                {
                    'name': 'Total Users',
                    'object_name': 'users',
                    'count': UserProfile.objects.count(),
                    'admin_url': reverse('admin:auth_user_changelist'),
                },
                {
                    'name': 'Total Comments',
                    'object_name': 'comments',
                    'count': Comment.objects.count(),
                    'admin_url': reverse('admin:projects_comment_changelist'),
                },
                {
                    'name': 'Total Claps',
                    'object_name': 'claps',
                    'count': Clap.objects.count(),
                    'admin_url': '#',
                },
            ]
        })
        
        return app_list

# Register the custom admin site
admin_site = CustomAdminSite(name='admin')
admin_site.register(Project, ProjectAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Notification, NotificationAdmin)
admin_site.register(ProjectAnalytics, ProjectAnalyticsAdmin)

# Contents from: .\apps.py
from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"


# Contents from: .\combine.py
import os

def get_files_recursively(directory, extensions):
    """
    Recursively get all files with specified extensions from directory and subdirectories.
    Uses os.walk() to traverse through all subdirectories at any depth.
    Excludes any directories named 'migrations'.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        # Exclude 'migrations' folders from the search
        dirs[:] = [d for d in dirs if d != '.venv']
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(root, file))
    return file_list

def combine_files(output_file, file_list):
    """
    Combine contents of all files in file_list into output_file
    """
    with open(output_file, 'a', encoding='utf-8') as outfile:
        for fname in file_list:
            # Add a header comment to show which file's contents follow
            outfile.write(f"\n\n# Contents from: {fname}\n")
            try:
                with open(fname, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        outfile.write(line)
            except Exception as e:
                outfile.write(f"# Error reading file {fname}: {str(e)}\n")

def main():
    # Define the base directory (current directory in this case)
    base_directory = "."
    output_file = 'combined.py'
    extensions = ('.py', '.html', '.css', '.js')

    # Remove output file if it exists
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception as e:
            print(f"Error removing existing {output_file}: {str(e)}")
            return

    # Get all files recursively - os.walk() will traverse through all subdirectories
    all_files = get_files_recursively(base_directory, extensions)
    
    # Sort files by extension and then by name
    all_files.sort(key=lambda x: (os.path.splitext(x)[1], x))

    # Add a header to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# Combined Python and HTML files\n")
        outfile.write(f"# Generated from directory: {os.path.abspath(base_directory)}\n")
        outfile.write(f"# Total files found: {len(all_files)}\n\n")

    # Combine all files
    combine_files(output_file, all_files)
    
    print(f"Successfully combined {len(all_files)} files into {output_file}")
    print("Files processed:")
    for file in all_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()

# Contents from: .\context_processors.py
# projects/context_processors.py

from django.conf import settings
from .models import Project, UserProfile

def site_context(request):
    """
    Add common context variables to all templates
    """
    context = {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
    }
    
    if request.user.is_authenticated:
        # Get unread notifications count
        context['unread_notifications_count'] = request.user.notifications.filter(
            is_read=False
        ).count()
        
        # Get user's bookmarked projects
        context['bookmarked_projects'] = Project.objects.filter(
            bookmarks__user=request.user
        ).values_list('id', flat=True)
        
        # Check if user has completed their profile
        try:
            profile = request.user.profile
            context['profile_completed'] = all([
                profile.bio,
                profile.location,
                profile.avatar
            ])
        except UserProfile.DoesNotExist:
            context['profile_completed'] = False
    
    return context

def notifications_processor(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        recent_notifications = request.user.notifications.all()[:5]
        return {
            'unread_notifications_count': unread_count,
            'notifications': recent_notifications,
        }
    return {}

# Contents from: .\filters\__init__.py
from .project_filters import ProjectFilter

__all__ = ['ProjectFilter']


# Contents from: .\filters\project_filters.py
import django_filters
from django.db.models import Q
from ..models import Project

class ProjectFilter(django_filters.FilterSet):
    """FilterSet for advanced project filtering"""
    query = django_filters.CharFilter(method='filter_query')
    tags = django_filters.CharFilter(method='filter_tags')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_claps = django_filters.NumberFilter(field_name='claps', lookup_expr='gte')
    has_github = django_filters.BooleanFilter(method='filter_has_github')
    
    class Meta:
        model = Project
        fields = ['query', 'tags', 'date_from', 'date_to', 'min_claps', 'has_github']
    
    def filter_query(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value) |
            Q(tags__icontains=value)
        )
    
    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        
        tags = [tag.strip().lower() for tag in value.split(',') if tag.strip()]
        for tag in tags:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset
    
    def filter_has_github(self, queryset, name, value):
        if value:
            return queryset.exclude(github_link='')
        return queryset

# Contents from: .\forms.py
# projects/forms.py

from django import forms
from django.core.validators import URLValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, Q
import mimetypes
from PIL import Image
from io import BytesIO
import os

from .models import (
    Project,
    Comment,
    UserProfile,
    Rating,
    Bookmark,
    ProjectAnalytics,
    Notification,
    Profile
)

class ProjectForm(forms.ModelForm):
    """
    Form for creating and editing projects.
    Includes validation for GitHub links and tag formatting.
    """
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., AI, Machine Learning, NLP)',
            'data-toggle': 'tooltip',
            'title': 'Add up to 5 tags to help others find your project'
        })
    )
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'tags', 'pdf_file', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title',
                'maxlength': '200',
                'data-toggle': 'tooltip',
                'title': 'Choose a descriptive title for your project'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project in detail...',
                'data-toggle': 'tooltip',
                'title': 'Explain what your project does, technologies used, and its purpose'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repository',
                'data-toggle': 'tooltip',
                'title': 'Link to your GitHub repository'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf',
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }

    def clean_github_link(self):
        """Validate GitHub repository URL"""
        url = self.cleaned_data['github_link']
        if not url.startswith(('https://github.com/', 'http://github.com/')):
            raise ValidationError('Please enter a valid GitHub repository URL')
        
        try:
            URLValidator()(url)
        except ValidationError:
            raise ValidationError('Please enter a valid URL')
        
        return url

    def clean_tags(self):
        """Validate and format tags"""
        tags = self.cleaned_data['tags']
        if not tags:
            return ''
        
        # Clean and validate tags
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = [x for x in tag_list if not (x in seen or seen.add(x))]
        
        if len(unique_tags) > 5:
            raise ValidationError('Please enter no more than 5 unique tags')
        
        if any(len(tag) > 20 for tag in unique_tags):
            raise ValidationError('Each tag must be less than 20 characters')
        
        return ', '.join(unique_tags)

    def clean_pdf_file(self):
        """Validate PDF file"""
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            # Check file size (10MB limit)
            if pdf_file.size > 10 * 1024 * 1024:
                raise ValidationError('PDF file must be smaller than 10MB')

            # Check file extension
            ext = os.path.splitext(pdf_file.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError('Only PDF files are allowed')

            # Check MIME type using mimetypes
            file_type, encoding = mimetypes.guess_type(pdf_file.name)
            if file_type != 'application/pdf':
                raise ValidationError('Invalid PDF file')

        return pdf_file

    def clean_featured_image(self):
        """Validate and process featured image"""
        image = self.cleaned_data.get('featured_image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 5MB')

            try:
                img = Image.open(image)
                
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Check dimensions
                if img.width > 2000 or img.height > 2000:
                    raise ValidationError('Image dimensions should not exceed 2000x2000 pixels')
                
                # Resize if larger than 1200px
                if img.width > 1200 or img.height > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                # Save optimized image
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Return processed image
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(image.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return image

class CommentForm(forms.ModelForm):
    """
    Form for adding comments to projects.
    Includes validation for minimum content length.
    """
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...',
                'data-toggle': 'tooltip',
                'title': 'Share your thoughts, feedback, or questions'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_content(self):
        """Validate comment content"""
        content = self.cleaned_data['content'].strip()
        if len(content) < 10:
            raise ValidationError('Comment must be at least 10 characters long')
        if len(content) > 1000:
            raise ValidationError('Comment must be less than 1000 characters')
        return content

    def clean_image(self):
        """Validate comment image"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (2MB limit)
            if image.size > 2 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 2MB')

            try:
                img = Image.open(image)
                
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Check dimensions
                if img.width > 1000 or img.height > 1000:
                    raise ValidationError('Image dimensions should not exceed 1000x1000 pixels')
                
                # Resize if larger than 800px
                if img.width > 800 or img.height > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                # Save optimized image
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                # Return processed image
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(image.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return image

class UserProfileForm(forms.ModelForm):
    """Form for user profile management"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website', 'github_username', 'linkedin_url', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'maxlength': '500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where are you based?',
                'maxlength': '100'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username',
                'maxlength': '39'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.linkedin.com/in/your-profile'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_avatar(self):
        """Validate avatar file"""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (5MB limit)
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError('Avatar file must be smaller than 5MB')

            try:
                img = Image.open(avatar)
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Resize to standard avatar size
                output_size = (300, 300)
                img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
                from django.core.files.uploadedfile import InMemoryUploadedFile
                return InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(avatar.name)[0]}.jpg",
                    'image/jpeg',
                    output.tell(),
                    None
                )
            except Exception as e:
                raise ValidationError(f'Invalid image file: {str(e)}')
        return avatar

class RatingForm(forms.ModelForm):
    """Form for rating projects"""
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Rating score'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience with this project (optional)',
                'maxlength': 500
            })
        }

    def clean_review(self):
        review = self.cleaned_data.get('review', '').strip()
        if len(review) > 500:
            raise ValidationError('Review must be less than 500 characters')
        return review

class BookmarkForm(forms.ModelForm):
    """Form for managing bookmarks"""
    class Meta:
        model = Bookmark
        fields = ['project']
        widgets = {
            'project': forms.HiddenInput()
        }

class ProjectSearchForm(forms.Form):
    """Form for project search and filtering"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search seeds...',
            'aria-label': 'Search'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by tags (comma separated)',
            'aria-label': 'Tags'
        })
    )
    
    SORT_CHOICES = [
        ('-created_at', 'Newest first'),
        ('created_at', 'Oldest first'),
        ('-claps', 'Most popular'),
        ('title', 'Alphabetical'),
    ]
    
    sort = forms.ChoiceField(
        required=False,
        initial='-created_at',
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Sort projects'
        })
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            return [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        return []
    

################################

class FileValidationMixin:
    """Mixin for common file validation methods"""
    
    def validate_file_size(self, file, max_size_mb=5):
        if file.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f'File size must be no more than {max_size_mb}MB')
    
    def validate_file_type(self, file, allowed_types):
        file_type = mimetypes.guess_type(file.name)[0]
        if file_type not in allowed_types:
            raise ValidationError(f'File type {file_type} is not supported')
    
    def validate_image(self, image, max_dimension=2000):
        try:
            img = Image.open(image)
            if img.width > max_dimension or img.height > max_dimension:
                raise ValidationError(f'Image dimensions should not exceed {max_dimension}x{max_dimension} pixels')
            return img
        except Exception as e:
            raise ValidationError(f'Invalid image file: {str(e)}')

class AdvancedSearchForm(forms.Form):
    """Advanced search form with multiple filters"""
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, description, or author'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-role': 'tagsinput'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    min_claps = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    has_github = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-claps', 'Most popular'),
            ('-comment_count', 'Most discussed'),
            ('title', 'Alphabetical'),
            ('-rating_avg', 'Highest rated')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise ValidationError("End date should be greater than start date")
        
        return cleaned_data

# projects/filters.py

import django_filters
from django.db.models import Avg, Count, Q
from .models import Project

class ProjectFilter(django_filters.FilterSet):
    """FilterSet for advanced project filtering"""
    query = django_filters.CharFilter(method='filter_query')
    tags = django_filters.CharFilter(method='filter_tags')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_claps = django_filters.NumberFilter(field_name='claps', lookup_expr='gte')
    has_github = django_filters.BooleanFilter(method='filter_has_github')
    
    class Meta:
        model = Project
        fields = ['query', 'tags', 'date_from', 'date_to', 'min_claps', 'has_github']
    
    def filter_query(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value) |
            Q(tags__icontains=value)
        )
    
    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        
        tags = [tag.strip().lower() for tag in value.split(',') if tag.strip()]
        for tag in tags:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset
    
    def filter_has_github(self, queryset, name, value):
        if value:
            return queryset.exclude(github_link='')
        return queryset

# Now let's update the views.py to use these filters:

class NotificationSettingsForm(forms.Form):
    email_on_comment = forms.BooleanField(
        required=False,
        label='Email me when someone comments on my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_follow = forms.BooleanField(
        required=False,
        label='Email me when someone follows me',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_clap = forms.BooleanField(
        required=False,
        label='Email me when someone claps for my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_bookmark = forms.BooleanField(
        required=False,
        label='Email me when someone bookmarks my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Profile
        fields = [
            'bio', 
            'location', 
            'website', 
            'github_username', 
            'twitter_username', 
            'avatar'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where are you based?'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username'
            }),
            'twitter_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Twitter username'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return avatar


# Contents from: .\migrations\0001_initial.py
# Generated by Django 5.1.3 on 2024-11-17 21:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("github_link", models.URLField()),
                ("tags", models.CharField(blank=True, max_length=100)),
                ("claps", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="projects.comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="projects.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Clap",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("clapped_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="claps_set",
                        to="projects.project",
                    ),
                ),
            ],
        ),
    ]


# Contents from: .\migrations\0002_alter_comment_options_alter_project_options_and_more.py
# Generated by Django 5.1.3 on 2024-11-17 22:18

import django.core.validators
import projects.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="comment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="project",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name="project",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="github_link",
            field=models.URLField(
                validators=[
                    django.core.validators.URLValidator(),
                    projects.models.validate_github_url,
                ]
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="tags",
            field=models.CharField(
                blank=True, help_text="Enter tags separated by commas", max_length=100
            ),
        ),
        migrations.AlterUniqueTogether(
            name="clap",
            unique_together={("project", "user")},
        ),
    ]


# Contents from: .\migrations\0003_userprofile.py
# Generated by Django 5.1.3 on 2024-11-17 22:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_alter_comment_options_alter_project_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=500)),
                ("location", models.CharField(blank=True, max_length=100)),
                ("github_username", models.CharField(blank=True, max_length=100)),
                ("linkedin_url", models.URLField(blank=True)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatars/"),
                ),
                ("website", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]


# Contents from: .\migrations\0004_notification.py
# Generated by Django 5.1.3 on 2024-11-17 22:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_userprofile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("clap", "Clap"),
                            ("comment", "Comment"),
                            ("reply", "Reply"),
                            ("mention", "Mention"),
                            ("follow", "Follow"),
                        ],
                        max_length=20,
                    ),
                ),
                ("message", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.comment",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]


# Contents from: .\migrations\0005_remove_notification_comment_and_more.py
# Generated by Django 5.1.3 on 2024-11-17 23:06

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_notification"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="comment",
        ),
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("clap", "Clap"),
                    ("comment", "Comment"),
                    ("reply", "Reply"),
                    ("mention", "Mention"),
                    ("follow", "Follow"),
                    ("rating", "Rating"),
                    ("bookmark", "Bookmark"),
                ],
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="ProjectAnalytics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("view_count", models.PositiveIntegerField(default=0)),
                ("unique_visitors", models.PositiveIntegerField(default=0)),
                ("github_clicks", models.PositiveIntegerField(default=0)),
                ("avg_time_spent", models.DurationField(default=datetime.timedelta)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("direct_traffic", models.PositiveIntegerField(default=0)),
                ("social_traffic", models.PositiveIntegerField(default=0)),
                ("search_traffic", models.PositiveIntegerField(default=0)),
                ("referral_traffic", models.PositiveIntegerField(default=0)),
                ("desktop_visits", models.PositiveIntegerField(default=0)),
                ("mobile_visits", models.PositiveIntegerField(default=0)),
                ("tablet_visits", models.PositiveIntegerField(default=0)),
                ("chrome_visits", models.PositiveIntegerField(default=0)),
                ("firefox_visits", models.PositiveIntegerField(default=0)),
                ("safari_visits", models.PositiveIntegerField(default=0)),
                ("edge_visits", models.PositiveIntegerField(default=0)),
                ("other_browsers", models.PositiveIntegerField(default=0)),
                ("unique_visitors_weekly", models.PositiveIntegerField(default=0)),
                ("unique_visitors_monthly", models.PositiveIntegerField(default=0)),
                ("github_clicks_weekly", models.PositiveIntegerField(default=0)),
                ("github_clicks_monthly", models.PositiveIntegerField(default=0)),
                (
                    "project",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analytics",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Project analytics",
            },
        ),
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "notes",
                    models.TextField(
                        blank=True, help_text="Add private notes about this project"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "project")},
            },
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        choices=[
                            (1, "1 - Poor"),
                            (2, "2 - Fair"),
                            (3, "3 - Good"),
                            (4, "4 - Very Good"),
                            (5, "5 - Excellent"),
                        ]
                    ),
                ),
                ("review", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "user")},
            },
        ),
    ]


# Contents from: .\migrations\0006_alter_bookmark_options_remove_bookmark_notes.py
# Generated by Django 5.1.3 on 2024-11-17 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_remove_notification_comment_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bookmark",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RemoveField(
            model_name="bookmark",
            name="notes",
        ),
    ]


# Contents from: .\migrations\0007_rename_clapped_at_clap_created_at_bookmark_notes_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 04:04

import django.core.validators
import projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0006_alter_bookmark_options_remove_bookmark_notes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clap",
            old_name="clapped_at",
            new_name="created_at",
        ),
        migrations.AddField(
            model_name="bookmark",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Upload an image (optional)",
                null=True,
                upload_to=projects.models.comment_image_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="additional_files",
            field=models.FileField(
                blank=True,
                help_text="Upload additional files (PDF, DOC, TXT, ZIP - max 10MB)",
                null=True,
                upload_to=projects.models.project_file_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf", "doc", "docx", "txt", "zip"]
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="featured_image",
            field=models.ImageField(
                blank=True,
                help_text="Upload a featured image for your project",
                null=True,
                upload_to=projects.models.project_image_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="pdf_file",
            field=models.FileField(
                blank=True,
                help_text="Upload a PDF document (max 10MB)",
                null=True,
                upload_to=projects.models.project_file_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf"]
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to=projects.models.avatar_upload_path
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="github_username",
            field=models.CharField(blank=True, max_length=39),
        ),
    ]


# Contents from: .\migrations\0008_alter_notification_notification_type_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 04:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_rename_clapped_at_clap_created_at_bookmark_notes_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("comment", "Comment"),
                    ("follow", "Follow"),
                    ("clap", "Clap"),
                    ("bookmark", "Bookmark"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]


# Contents from: .\migrations\0009_follow.py
# Generated by Django 5.1.3 on 2024-11-18 04:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0008_alter_notification_notification_type_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "following",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("follower", "following")},
            },
        ),
    ]


# Contents from: .\migrations\__init__.py


# Contents from: .\models.py
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
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def project_count(self):
        return self.user.project_set.count()
    
    @property
    def total_claps_received(self):
        return sum(project.claps for project in self.user.project_set.all())

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    twitter_username = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Notification settings
    email_on_comment = models.BooleanField(default=True)
    email_on_follow = models.BooleanField(default=True)
    email_on_clap = models.BooleanField(default=False)
    email_on_bookmark = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

# Contents from: .\serializers.py
# projects/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Project,
    Comment,
    UserProfile,
    Rating,
    Bookmark,
    ProjectAnalytics,
    Notification
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'bio', 'location', 'website',
            'github_username', 'linkedin_url', 'avatar'
        ]

class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tag_list = serializers.ListField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description',
            'github_link', 'tags', 'author',
            'claps', 'created_at', 'updated_at',
            'pdf_file', 'featured_image',
            'additional_files', 'tag_list',
            'comment_count', 'average_rating'
        ]
        read_only_fields = ['slug', 'claps']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'project', 'user', 'parent',
            'content', 'image', 'created_at',
            'updated_at', 'replies'
        ]
        read_only_fields = ['user']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = [
            'id', 'project', 'user', 'score',
            'review', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

class BookmarkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'project', 'created_at', 'notes']
        read_only_fields = ['user']

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'sender', 'project',
            'notification_type', 'message', 'is_read',
            'created_at'
        ]
        read_only_fields = ['recipient', 'sender', 'project']

class ProjectAnalyticsSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    device_distribution = serializers.SerializerMethodField()
    browser_distribution = serializers.SerializerMethodField()
    traffic_sources = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectAnalytics
        fields = [
            'project', 'view_count', 'unique_visitors',
            'github_clicks', 'avg_time_spent',
            'direct_traffic', 'social_traffic',
            'search_traffic', 'referral_traffic',
            'desktop_visits', 'mobile_visits',
            'tablet_visits', 'chrome_visits',
            'firefox_visits', 'safari_visits',
            'edge_visits', 'other_browsers',
            'unique_visitors_weekly', 'unique_visitors_monthly',
            'github_clicks_weekly', 'github_clicks_monthly',
            'device_distribution', 'browser_distribution',
            'traffic_sources', 'last_updated'
        ]
        read_only_fields = ['project']
    
    def get_device_distribution(self, obj):
        total = obj.desktop_visits + obj.mobile_visits + obj.tablet_visits
        if total == 0:
            return {
                'desktop': 0,
                'mobile': 0,
                'tablet': 0
            }
        
        return {
            'desktop': round((obj.desktop_visits / total) * 100, 1),
            'mobile': round((obj.mobile_visits / total) * 100, 1),
            'tablet': round((obj.tablet_visits / total) * 100, 1)
        }
    
    def get_browser_distribution(self, obj):
        total = (
            obj.chrome_visits + obj.firefox_visits +
            obj.safari_visits + obj.edge_visits + obj.other_browsers
        )
        
        if total == 0:
            return {
                'chrome': 0,
                'firefox': 0,
                'safari': 0,
                'edge': 0,
                'other': 0
            }
        
        return {
            'chrome': round((obj.chrome_visits / total) * 100, 1),
            'firefox': round((obj.firefox_visits / total) * 100, 1),
            'safari': round((obj.safari_visits / total) * 100, 1),
            'edge': round((obj.edge_visits / total) * 100, 1),
            'other': round((obj.other_browsers / total) * 100, 1)
        }
    
    def get_traffic_sources(self, obj):
        total = (
            obj.direct_traffic + obj.social_traffic +
            obj.search_traffic + obj.referral_traffic
        )
        
        if total == 0:
            return {
                'direct': 0,
                'social': 0,
                'search': 0,
                'referral': 0
            }
        
        return {
            'direct': round((obj.direct_traffic / total) * 100, 1),
            'social': round((obj.social_traffic / total) * 100, 1),
            'search': round((obj.search_traffic / total) * 100, 1),
            'referral': round((obj.referral_traffic / total) * 100, 1)
        }

class ProjectAnalyticsSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for analytics summary"""
    class Meta:
        model = ProjectAnalytics
        fields = ['view_count', 'unique_visitors', 'github_clicks']

# Contents from: .\templatetags\search_tags.py
# projects/templatetags/search_tags.py

from django import template
from django.utils.html import mark_safe
from django.utils.html import escape
import re

register = template.Library()

@register.filter(name='highlight')
def highlight_search_term(text, search_term):
    """Highlight search terms in text while preserving HTML safety"""
    if not search_term or not text:
        return text
    
    text = str(text)
    search_term = str(search_term)
    
    # Escape HTML in the text
    text = escape(text)
    
    # Create a pattern that matches whole words
    pattern = r'({})'.format(re.escape(search_term))
    
    # Replace matches with highlighted version
    highlighted = re.sub(
        pattern,
        r'<mark class="highlight">\1</mark>',
        text,
        flags=re.IGNORECASE
    )
    
    return mark_safe(highlighted)

@register.filter(name='querystring_without')
def querystring_without(query_dict, key):
    """Remove a key from querystring while preserving other parameters"""
    query_dict = query_dict.copy()
    query_dict.pop(key, None)
    return query_dict.urlencode()

@register.simple_tag
def url_with_querystring(request, **kwargs):
    """Build URL with updated querystring parameters"""
    query_dict = request.GET.copy()
    for key, value in kwargs.items():
        query_dict[key] = value
    return '?{}'.format(query_dict.urlencode())

# Contents from: .\tests.py
from django.test import TestCase

# Create your tests here.


# Contents from: .\urls.py
# projects/urls.py

from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # Project Management
    path('', views.project_list, name='project_list'),  # Main page to list projects
    path('submit/', views.submit_project, name='submit_project'),  # Page to submit a new project
    path('search/', views.search_projects, name='search_projects'),  # Page to search for projects
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),  # Page to view project leaderboard
    
    # Project Detail & Actions
    path('project/<int:pk>/', views.project_detail, name='project_detail'),  # View details of a specific project
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),  # Edit a specific project
    path('project/<int:pk>/rate/', views.rate_project, name='rate_project'),  # Rate a specific project
    path('project/<int:pk>/bookmark/', views.bookmark_project, name='bookmark_project'),  # Bookmark a specific project
    path('project/<int:pk>/clap/', views.clap_project, name='clap_project'),  # Clap for a specific project
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),  # Delete a specific project
    
    # Analytics
    path('project/<int:pk>/analytics/', views.ProjectAnalyticsView.as_view(), name='project_analytics'),  # View project analytics
    path('project/<int:pk>/analytics/data/', views.analytics_data, name='analytics_data'),  # Get analytics data for a project
    path('project/<int:pk>/analytics/export/csv/', views.export_analytics_csv, name='export_analytics_csv'),  # Export analytics as CSV
    path('project/<int:pk>/analytics/export/pdf/', views.export_analytics_pdf, name='export_analytics_pdf'),  # Export analytics as PDF
    
    # User Profiles - Note the reordered URLs
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit user profile
    path('profile/settings/', views.profile_settings, name='profile_settings'),  # User profile settings
    path('profile/<str:username>/', views.user_profile, name='user_profile'),  # View a user's profile
    path('profile/<str:username>/projects/', views.user_projects, name='user_projects'),  # View projects by a user
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),  # Follow a user
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),  # Unfollow a user
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),  # View user notifications
    path('notifications/<int:notification_id>/mark-read/', 
         views.mark_notification_read, name='mark_notification_read'),  # Mark a notification as read
    path('notifications/mark-all-read/', 
         views.mark_all_notifications_read, name='mark_all_notifications_read'),  # Mark all notifications as read
    
    # Comments
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),  # Delete a comment
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),  # Edit a comment
    
    # API Endpoints
    path('api/projects/', views.ProjectListAPI.as_view(), name='api_project_list'),  # API to list projects
    path('api/projects/<int:pk>/', views.ProjectDetailAPI.as_view(), name='api_project_detail'),  # API to get project details
    path('api/projects/<int:pk>/analytics/', views.ProjectAnalyticsAPI.as_view(), name='api_project_analytics'),  # API for project analytics
]

# Contents from: .\utils\__init__.py
# This file can be empty

# Contents from: .\utils\emails.py
# projects/utils/emails.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_notification_email(notification):
    """Send email for a new notification"""
    subject = f'New notification from {settings.SITE_NAME}'
    context = {
        'notification': notification,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/notification.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [notification.recipient.email],
        html_message=html_message,
        fail_silently=True
    )

def send_welcome_email(user):
    """Send welcome email to new users"""
    subject = f'Welcome to {settings.SITE_NAME}'
    context = {
        'user': user,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

def send_comment_notification(comment):
    """Send email notification for new comments"""
    subject = f'New comment on your project - {settings.SITE_NAME}'
    context = {
        'comment': comment,
        'project': comment.project,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/project_comment.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [comment.project.author.email],
        html_message=html_message,
        fail_silently=True
    )

def send_clap_notification(clap):
    """Send email notification for new claps"""
    subject = f'Someone appreciated your project - {settings.SITE_NAME}'
    context = {
        'clap': clap,
        'project': clap.project,
        'site_url': settings.SITE_URL,
        'unsubscribe_url': f"{settings.SITE_URL}/settings/notifications/"
    }
    
    html_message = render_to_string('emails/project_clap.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [clap.project.author.email],
        html_message=html_message,
        fail_silently=True
    )

# Contents from: .\utils\pdf.py
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

def generate_analytics_pdf(project, analytics_data):
    """Generate a PDF report for project analytics"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph(f"Analytics Report: {project.title}", title_style))
    story.append(Spacer(1, 12))

    # Overview Section
    story.append(Paragraph("Overview", styles['Heading2']))
    overview_data = [
        ["Total Views", str(analytics_data.get('view_count', 0))],
        ["Unique Visitors", str(analytics_data.get('unique_visitors', 0))],
        ["GitHub Clicks", str(analytics_data.get('github_clicks', 0))],
    ]
    overview_table = Table(overview_data, colWidths=[2*inch, 2*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 20))

    # Traffic Sources
    story.append(Paragraph("Traffic Sources", styles['Heading2']))
    traffic_data = [
        ["Direct", f"{analytics_data.get('direct_traffic', 0)}%"],
        ["Social", f"{analytics_data.get('social_traffic', 0)}%"],
        ["Search", f"{analytics_data.get('search_traffic', 0)}%"],
        ["Referral", f"{analytics_data.get('referral_traffic', 0)}%"],
    ]
    traffic_table = Table(traffic_data, colWidths=[2*inch, 2*inch])
    traffic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(traffic_table)
    story.append(Spacer(1, 20))

    # Device Distribution
    story.append(Paragraph("Device Distribution", styles['Heading2']))
    device_data = [
        ["Desktop", f"{analytics_data.get('desktop_visits', 0)}%"],
        ["Mobile", f"{analytics_data.get('mobile_visits', 0)}%"],
        ["Tablet", f"{analytics_data.get('tablet_visits', 0)}%"],
    ]
    device_table = Table(device_data, colWidths=[2*inch, 2*inch])
    device_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(device_table)

    # Build PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# Contents from: .\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, Avg, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.core.cache import cache
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.core.files.storage import default_storage
import csv
import json
import os
import pytz
from datetime import datetime, timedelta
from io import StringIO
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer, ProjectAnalyticsSerializer, ProjectAnalyticsSummarySerializer

from .models import (
    Project, Comment, Clap, UserProfile, Rating, 
    Bookmark, ProjectAnalytics, Notification, Follow
)
from .forms import (
    ProjectForm, CommentForm, ProjectSearchForm, UserProfileForm,
    RatingForm, BookmarkForm, AdvancedSearchForm, ProfileForm, NotificationSettingsForm
)
from .filters.project_filters import ProjectFilter
from django.contrib.auth.forms import UserCreationForm
from .utils.pdf import generate_analytics_pdf

class ProjectAnalyticsView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_analytics.html'
    context_object_name = 'project'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analytics = self.object.analytics
        now = timezone.now()
        
        # Calculate date ranges
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Get weekly and monthly stats
        weekly_stats = {
            'views': analytics.get_views_count(since=week_ago),
            'unique_visitors': analytics.get_unique_visitors_count(since=week_ago),
            'github_clicks': analytics.get_github_clicks_count(since=week_ago),
            'comments': self.object.comments.filter(created_at__gte=week_ago).count(),
            'claps': self.object.claps_set.filter(created_at__gte=week_ago).count(),
            'ratings': self.object.ratings.filter(created_at__gte=week_ago).count()
        }
        
        monthly_stats = {
            'views': analytics.get_views_count(since=month_ago),
            'unique_visitors': analytics.get_unique_visitors_count(since=month_ago),
            'github_clicks': analytics.get_github_clicks_count(since=month_ago),
            'comments': self.object.comments.filter(created_at__gte=month_ago).count(),
            'claps': self.object.claps_set.filter(created_at__gte=month_ago).count(),
            'ratings': self.object.ratings.filter(created_at__gte=month_ago).count()
        }
        
        # Calculate trends
        def calculate_trend(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 1)

        trends = {
            'views': calculate_trend(
                weekly_stats['views'], 
                analytics.get_views_count(since=week_ago - timedelta(days=7), until=week_ago)
            ),
            'visitors': calculate_trend(
                weekly_stats['unique_visitors'],
                analytics.get_unique_visitors_count(since=week_ago - timedelta(days=7), until=week_ago)
            ),
            'github': calculate_trend(
                weekly_stats['github_clicks'],
                analytics.get_github_clicks_count(since=week_ago - timedelta(days=7), until=week_ago)
            )
        }
        
        # Get traffic sources breakdown
        total_traffic = (
            analytics.direct_traffic + 
            analytics.social_traffic + 
            analytics.search_traffic + 
            analytics.referral_traffic
        )
        
        traffic_sources = {
            'direct': {
                'count': analytics.direct_traffic,
                'percentage': round((analytics.direct_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            },
            'social': {
                'count': analytics.social_traffic,
                'percentage': round((analytics.social_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            },
            'search': {
                'count': analytics.search_traffic,
                'percentage': round((analytics.search_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            },
            'referral': {
                'count': analytics.referral_traffic,
                'percentage': round((analytics.referral_traffic / total_traffic * 100), 1) if total_traffic > 0 else 0
            }
        }
        
        # Device and browser stats
        total_visits = (
            analytics.desktop_visits + 
            analytics.mobile_visits + 
            analytics.tablet_visits
        )
        
        devices = {
            'desktop': {
                'count': analytics.desktop_visits,
                'percentage': round((analytics.desktop_visits / total_visits * 100), 1) if total_visits > 0 else 0
            },
            'mobile': {
                'count': analytics.mobile_visits,
                'percentage': round((analytics.mobile_visits / total_visits * 100), 1) if total_visits > 0 else 0
            },
            'tablet': {
                'count': analytics.tablet_visits,
                'percentage': round((analytics.tablet_visits / total_visits * 100), 1) if total_visits > 0 else 0
            }
        }
        
        total_browser_visits = (
            analytics.chrome_visits +
            analytics.firefox_visits +
            analytics.safari_visits +
            analytics.edge_visits +
            analytics.other_browsers
        )
        
        browsers = [
            {
                'name': 'Chrome',
                'count': analytics.chrome_visits,
                'percentage': round((analytics.chrome_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#4285F4',
                'icon': 'browser-chrome'
            },
            {
                'name': 'Firefox',
                'count': analytics.firefox_visits,
                'percentage': round((analytics.firefox_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#FF7139',
                'icon': 'browser-firefox'
            },
            {
                'name': 'Safari',
                'count': analytics.safari_visits,
                'percentage': round((analytics.safari_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#000000',
                'icon': 'browser-safari'
            },
            {
                'name': 'Edge',
                'count': analytics.edge_visits,
                'percentage': round((analytics.edge_visits / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#0078D7',
                'icon': 'browser-edge'
            },
            {
                'name': 'Other',
                'count': analytics.other_browsers,
                'percentage': round((analytics.other_browsers / total_browser_visits * 100), 1) if total_browser_visits > 0 else 0,
                'color': '#6B7280',
                'icon': 'browser'
            }
        ]
        
        # Get time series data for charts
        time_series_data = analytics.get_time_series_data(days=30)
        
        context.update({
            'analytics': analytics,
            'weekly_stats': weekly_stats,
            'monthly_stats': monthly_stats,
            'trends': trends,
            'traffic_sources': traffic_sources,
            'devices': devices,
            'browsers': browsers,
            'time_series_data': time_series_data,
            'now': now
        })
        
        return context

def analytics_data(request, pk):
    """API endpoint for fetching analytics data"""
    project = get_object_or_404(Project, pk=pk)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    analytics = project.analytics
    time_range = request.GET.get('range', 'week')
    
    if time_range == 'week':
        days = 7
    elif time_range == 'month':
        days = 30
    else:
        days = 365
    
    data = analytics.get_time_series_data(days=days)
    
    return JsonResponse(data)

def export_analytics_csv(request, pk):
    """Export analytics data as CSV"""
    project = get_object_or_404(Project, pk=pk)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    analytics = project.analytics
    
    # Create CSV data
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Date', 'Views', 'Unique Visitors', 'GitHub Clicks',
        'Average Time (minutes)', 'Comments', 'Claps'
    ])
    
    # Get daily data for the last 30 days
    data = analytics.get_time_series_data(days=30)
    for entry in data['daily_data']:
        writer.writerow([
            entry['date'],
            entry['views'],
            entry['visitors'],
            entry['github_clicks'],
            round(entry['avg_time_spent'] / 60, 2),
            entry['comments'],
            entry['claps']
        ])
    
    # Create the HTTP response with CSV data
    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{project.slug}-analytics.csv"'
    
    return response

def export_analytics_pdf(request, pk):
    """Export analytics data as PDF"""
    if not request.method == 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    project = get_object_or_404(Project, pk=pk)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    data = json.loads(request.body)
    chart_images = data.get('charts', {})
    date_range = data.get('dateRange', 'week')
    
    # Generate PDF using the utility function
    pdf_file = generate_analytics_pdf(project, chart_images, date_range)
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{project.slug}-analytics.pdf"'
    
    return response

def get_popular_tags():
    """Helper function to get popular tags"""
    return (Project.objects
            .values('tags')
            .annotate(count=Count('id'))
            .order_by('-count')
            .exclude(tags='')[:10])

def get_client_info(request):
    """Get basic client information without user-agents package"""
    info = {
        'is_mobile': request.META.get('HTTP_USER_AGENT', '').lower().find('mobile') > -1,
        'browser': 'other',
        'ip': request.META.get('REMOTE_ADDR'),
        'referrer': request.META.get('HTTP_REFERER', ''),
    }
    
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    if 'chrome' in user_agent:
        info['browser'] = 'chrome'
    elif 'firefox' in user_agent:
        info['browser'] = 'firefox'
    elif 'safari' in user_agent:
        info['browser'] = 'safari'
    elif 'edge' in user_agent:
        info['browser'] = 'edge'
    
    return info

def update_analytics(request, project):
    """Update project analytics"""
    analytics, created = ProjectAnalytics.objects.get_or_create(project=project)
    client_info = get_client_info(request)
    
    # Update view count
    analytics.view_count += 1
    
    # Update device stats
    if client_info['is_mobile']:
        analytics.mobile_visits += 1
    else:
        analytics.desktop_visits += 1
    
    # Update browser stats
    if client_info['browser'] == 'chrome':
        analytics.chrome_visits += 1
    elif client_info['browser'] == 'firefox':
        analytics.firefox_visits += 1
    elif client_info['browser'] == 'safari':
        analytics.safari_visits += 1
    elif client_info['browser'] == 'edge':
        analytics.edge_visits += 1
    else:
        analytics.other_browsers += 1
    
    # Update traffic sources
    referrer = client_info['referrer']
    if not referrer:
        analytics.direct_traffic += 1
    elif 'google' in referrer or 'bing' in referrer:
        analytics.search_traffic += 1
    elif 'facebook' in referrer or 'twitter' in referrer or 'linkedin' in referrer:
        analytics.social_traffic += 1
    else:
        analytics.referral_traffic += 1
    
    # Update unique visitors
    visitor_key = f"visitor_{client_info['ip']}_{project.id}"
    if not cache.get(visitor_key):
        analytics.unique_visitors += 1
        cache.set(visitor_key, True, timeout=86400)  # 24 hours
        
        # Update weekly and monthly unique visitors
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        if not cache.get(f"{visitor_key}_weekly"):
            analytics.unique_visitors_weekly += 1
            cache.set(f"{visitor_key}_weekly", True, timeout=604800)  # 7 days
            
        if not cache.get(f"{visitor_key}_monthly"):
            analytics.unique_visitors_monthly += 1
            cache.set(f"{visitor_key}_monthly", True, timeout=2592000)  # 30 days
    
    analytics.save()

def project_list(request):
    """List and search projects"""
    search_form = ProjectSearchForm(request.GET)
    projects = Project.objects.all()
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        tags = search_form.cleaned_data.get('tags')
        sort = search_form.cleaned_data.get('sort')
        
        if query:
            projects = projects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(author__username__icontains=query) |
                Q(tags__icontains=query)
            )
        
        if tags:
            for tag in tags:
                projects = projects.filter(tags__icontains=tag)
        
        if sort:
            projects = projects.order_by(sort)
        else:
            projects = projects.order_by('-created_at')
    else:
        projects = projects.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(projects, 12)
    page = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    # Get popular tags
    popular_tags = (Project.objects
        .values_list('tags', flat=True)
        .exclude(tags='')
        .annotate(count=Count('id'))
        .order_by('-count')[:10])
    
    context = {
        'page_obj': page_obj,
        'popular_tags': popular_tags,
        'search_form': search_form,
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def submit_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            
            # Handle featured image
            if 'featured_image' in request.FILES:
                project.featured_image = form.cleaned_data['featured_image']
            
            project.save()
            
            # Create project directory
            project_dir = f'uploads/user_{request.user.id}/project_{project.id}'
            os.makedirs(os.path.join(settings.MEDIA_ROOT, project_dir), exist_ok=True)
            
            messages.success(request, 'Project submitted successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/submit_project.html', {'form': form})



def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    comments = project.comments.filter(parent=None).select_related('user').prefetch_related('replies')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            
            # Create notification for project author
            if project.author != request.user:
                Notification.objects.create(
                    recipient=project.author,
                    sender=request.user,
                    project=project,
                    notification_type='comment',
                    message=f"{request.user.username} commented on your project"
                )
            
            messages.success(request, 'Comment added successfully!')
            return redirect('project_detail', pk=pk)
    else:
        form = CommentForm()
    
    context = {
        'project': project,
        'comments': comments,
        'form': form,
    }
    return render(request, 'projects/project_detail.html', context)



@login_required
def rate_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        form = RatingForm(request.POST)
        
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                project=project,
                user=request.user,
                defaults={
                    'score': form.cleaned_data['score'],
                    'review': form.cleaned_data['review']
                }
            )
            
            # Update project rating cache
            avg_rating = project.ratings.aggregate(Avg('score'))['score__avg']
            cache.set(f'project_rating_{project.id}', avg_rating, timeout=3600)
            
            messages.success(request, 'Thank you for your rating!')
            return JsonResponse({
                'status': 'success',
                'rating': avg_rating,
                'total_ratings': project.ratings.count()
            })
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def toggle_bookmark(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(
        project=project,
        user=request.user,
        defaults={'notes': ''}
    )
    
    if not created:
        bookmark.delete()
        return JsonResponse({'status': 'removed'})
    
    return JsonResponse({'status': 'added'})

@login_required
def update_bookmark_notes(request, pk):
    bookmark = get_object_or_404(Bookmark, project_id=pk, user=request.user)
    
    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('project')
    return render(request, 'projects/bookmarks.html', {'bookmarks': bookmarks})



@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'projects/edit_profile.html', {'form': form})

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    projects = Project.objects.filter(author=profile_user).order_by('-created_at')
    
    # Get follow status
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()
    
    # Get counts
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    
    context = {
        'profile_user': profile_user,
        'projects': projects,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'projects/user_profile.html', context)

def user_projects(request, username):
    user = get_object_or_404(User, username=username)
    projects = user.project_set.all().order_by('-created_at')
    
    # Filter by tag if provided
    tag = request.GET.get('tag')
    if tag:
        projects = projects.filter(tags__icontains=tag)
    
    paginator = Paginator(projects, 10)
    page = request.GET.get('page')
    projects_page = paginator.get_page(page)
    
    context = {
        'user_profile': user,
        'projects': projects_page,
        'selected_tag': tag,
    }
    return render(request, 'projects/user_projects.html', context)

@login_required
def notifications(request):
    notifications_list = request.user.notifications.all().order_by('-created_at')
    return render(request, 'projects/notifications.html', {
        'notifications': notifications_list
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user != user_to_follow:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if created:
            # Create notification for the followed user
            Notification.objects.create(
                recipient=user_to_follow,
                sender=request.user,
                notification_type='follow',
                message=f'{request.user.username} started following you'
            )
    
    return redirect('projects:user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    
    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()
    
    return redirect('projects:user_profile', username=username)

def search_projects(request):
    """Advanced search view"""
    form = AdvancedSearchForm(request.GET)
    projects = Project.objects.all()
    
    if form.is_valid():
        # Apply filters using ProjectFilter
        project_filter = ProjectFilter(request.GET, queryset=projects)
        projects = project_filter.qs
        
        # Apply sorting
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            if sort_by == '-rating_avg':
                # Annotate with average rating
                projects = projects.annotate(
                    rating_avg=Avg('ratings__score')
                ).order_by('-rating_avg')
            elif sort_by == '-comment_count':
                # Annotate with comment count
                projects = projects.annotate(
                    comment_count=Count('comments')
                ).order_by('-comment_count')
            else:
                projects = projects.order_by(sort_by)
    
    # Annotate with additional metrics for display
    projects = projects.annotate(
        comment_count=Count('comments'),
        rating_avg=Avg('ratings__score')
    )
    
    # Pagination
    paginator = Paginator(projects, settings.MAX_PROJECTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    context = {
        'form': form,
        'projects': projects,
        'popular_tags': get_popular_tags(),
        'total_results': paginator.count,
    }
    
    if request.headers.get('HX-Request'):
        # Return partial template for HTMX requests
        return render(request, 'projects/includes/project_list_results.html', context)
    
    return render(request, 'projects/search.html', context)

@login_required
def bookmark_project(request, pk):
    """Add or remove a project bookmark"""
    project = get_object_or_404(Project, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        project=project
    )
    
    if not created:
        # If bookmark already existed, remove it
        bookmark.delete()
        messages.success(request, 'Bookmark removed.')
        return JsonResponse({
            'status': 'success',
            'action': 'removed',
            'message': 'Project removed from bookmarks'
        })
    
    # Create notification for project author
    if project.author != request.user:
        Notification.create_notification(
            recipient=project.author,
            sender=request.user,
            notification_type='bookmark',
            project=project
        )
    
    messages.success(request, 'Project bookmarked successfully.')
    return JsonResponse({
        'status': 'success',
        'action': 'added',
        'message': 'Project added to bookmarks'
    })

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

def get_monthly_contributions():
    """Calculate monthly contributions for all users"""
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    return User.objects.annotate(
        projects_count=Count(
            'project',
            filter=models.Q(project__created_at__gte=start_of_month)
        ),
        claps_received=Sum(
            'project__claps',
            filter=models.Q(project__created_at__gte=start_of_month)
        ),
        total_contributions=models.F('projects_count') + models.F('claps_received')
    ).filter(
        models.Q(projects_count__gt=0) | models.Q(claps_received__gt=0)
    ).order_by('-total_contributions')[:10]

def leaderboard_view(request):
    """View for the leaderboard page"""
    contributions = get_monthly_contributions()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON for React component
        data = [{
            'rank': idx + 1,
            'user': user.username,
            'contributions': user.total_contributions,
            'projects': user.projects_count,
            'claps': user.claps_received or 0,
            'change': 0  # Calculate change from previous position
        } for idx, user in enumerate(contributions)]
        return JsonResponse({'leaderboard': data})
    
    return render(request, 'projects/leaderboard.html', {
        'contributions': contributions
    })


#####
# views.py (add these methods)



@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('projects:project_list')
    return render(request, 'projects/delete_project.html', {'project': project})



@login_required
def clap_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        clap, created = Clap.objects.get_or_create(user=request.user, project=project)
        if created:
            project.claps += 1
            project.save()
            return JsonResponse({'status': 'success', 'claps': project.claps})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('projects:project_detail', pk=comment.project.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'projects/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user != request.user and comment.project.author != request.user:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    project_pk = comment.project.pk
    comment.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('projects:project_detail', pk=project_pk)

@login_required
def mark_all_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

# API Views
class ProjectListAPI(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class ProjectDetailAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class ProjectAnalyticsAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        project = super().get_object()
        if project.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return project.analytics

@login_required
def profile_settings(request):
    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST)
        if form.is_valid():
            # Update notification settings
            user_profile.email_on_comment = form.cleaned_data['email_on_comment']
            user_profile.email_on_follow = form.cleaned_data['email_on_follow']
            user_profile.email_on_clap = form.cleaned_data['email_on_clap']
            user_profile.email_on_bookmark = form.cleaned_data['email_on_bookmark']
            user_profile.save()
            
            messages.success(request, 'Settings updated successfully!')
            return redirect('projects:profile_settings')
    else:
        # Initialize form with current settings
        form = NotificationSettingsForm(initial={
            'email_on_comment': user_profile.email_on_comment,
            'email_on_follow': user_profile.email_on_follow,
            'email_on_clap': user_profile.email_on_clap,
            'email_on_bookmark': user_profile.email_on_bookmark,
        })

    return render(request, 'projects/profile_settings.html', {
        'form': form,
        'active_tab': 'settings'
    })