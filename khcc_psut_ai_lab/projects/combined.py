# Combined Python and HTML files
# Generated from directory: C:\Users\USER\Documents\khcc_psut_ai_lab\khcc_psut_ai_lab\projects
# Total files found: 77



# Contents from: .\__init__.py


# Contents from: .\admin.py
# projects/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Project, Comment, Clap, UserProfile, Rating,
    Bookmark, ProjectAnalytics, Notification, Follow
)
from allauth.account.models import EmailAddress
from django.contrib import messages

# Extend UserProfile admin to include faculty-specific fields
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Basic Information', {
            'fields': ('avatar', 'bio', 'location', 'website')
        }),
        ('Professional Information', {
            'fields': ('title', 'department', 'research_interests')
        }),
        ('Social Media', {
            'fields': ('github_username', 'linkedin_url', 'twitter_username')
        }),
        ('Notification Settings', {
            'fields': (
                'email_on_comment', 'email_on_follow',
                'email_on_clap', 'email_on_bookmark'
            ),
            'classes': ('collapse',)
        })
    )

class EmailAddressInline(admin.StackedInline):
    model = EmailAddress
    extra = 0
    can_delete = True
    verbose_name = 'Email Address'
    verbose_name_plural = 'Email Addresses'

# Customize the User admin to include profile information
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, EmailAddressInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_faculty_member', 'is_email_verified')
    list_filter = BaseUserAdmin.list_filter + ('groups__name', 'emailaddress__verified')
    actions = ['verify_email_action']
    
    def is_faculty_member(self, obj):
        return obj.groups.filter(name='Faculty').exists()
    is_faculty_member.boolean = True
    is_faculty_member.short_description = 'Faculty'
    
    def is_email_verified(self, obj):
        try:
            return obj.emailaddress_set.first().verified
        except AttributeError:
            return False
    is_email_verified.boolean = True
    is_email_verified.short_description = 'Email Verified'
    
    def verify_email_action(self, request, queryset):
        verified_count = 0
        for user in queryset:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={'verified': True, 'primary': True}
            )
            
            if not created and not email_address.verified:
                email_address.verified = True
                email_address.save()
                verified_count += 1

        self.message_user(
            request,
            f"Successfully verified email for {verified_count} users.",
            messages.SUCCESS
        )
    verify_email_action.short_description = "Verify email for selected users"

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

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
    list_display = ('user', 'title', 'department', 'is_faculty_member', 'created_at')
    list_filter = ('department', 'user__groups', 'created_at')
    search_fields = ('user__username', 'user__email', 'title', 'department')
    readonly_fields = ('created_at', 'updated_at')
    
    def is_faculty_member(self, obj):
        return obj.is_faculty
    is_faculty_member.boolean = True
    is_faculty_member.short_description = 'Faculty'

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

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')

class CustomAdminSite(admin.AdminSite):
    site_header = 'KHCC.AI Administration'
    site_title = 'KHCC.AI Admin'
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
admin_site.register(Follow, FollowAdmin)




# Contents from: .\apps.py
from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"

    def ready(self):
        import projects.signals  # Register signals when app is ready


# Contents from: .\combine.py
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
    extensions = ('.py')

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

# Contents from: .\decorators.py
# projects/decorators.py

from functools import wraps
from .models.analytics import EventTracker
import json

def track_event(event_type, get_metadata=None):
    """
    Decorator to track events
    
    @track_event('view')
    @track_event('action', get_metadata=lambda request, *args, **kwargs: {'project_id': kwargs.get('pk')})
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Get the response first
            response = view_func(request, *args, **kwargs)
            
            try:
                # Get metadata if function provided
                metadata = {}
                if get_metadata:
                    metadata = get_metadata(request, *args, **kwargs)
                
                # Create event
                EventTracker.objects.create(
                    event_type=event_type,
                    user=request.user if request.user.is_authenticated else None,
                    path=request.path,
                    target=request.POST.get('target', ''),
                    metadata=metadata
                )
            except Exception as e:
                # Log the error but don't affect the response
                print(f"Error tracking event: {str(e)}")
            
            return response
        return wrapped_view
    return decorator

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

from django import forms
from .models import (
    Project, Comment, UserProfile, Rating, Bookmark, 
    Notification, Startup, Product, Tool, Dataset,
    VirtualMember, Application, Sponsorship
)

from .models import (
    Project,
    Comment,
    UserProfile,
    Rating,
    Bookmark,
    ProjectAnalytics,
    Notification,
    Solution,
    Team
)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from khcc_psut_ai_lab.constants import TALENT_TYPES



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
        label='Email me when someone clap_count for my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    email_on_bookmark = forms.BooleanField(
        required=False,
        label='Email me when someone bookmarks my projects',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
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
        fields = [
            'title', 'description', 'github_link', 'tags',
            'pdf_file', 'featured_image', 'additional_files',
            'youtube_url', 'is_gold', 'token_reward',
            'gold_goal', 'deadline'
        ]
        widgets = {
            'deadline': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'tags': forms.TextInput(
                attrs={'placeholder': 'Enter tags separated by commas'}
            ),
            'gold_goal': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        # Only show gold seed fields to faculty members
        if self.user and not self.user.groups.filter(name='Faculty').exists():
            self.fields.pop('is_gold', None)
            self.fields.pop('token_reward', None)
            self.fields.pop('gold_goal', None)
            self.fields.pop('deadline', None)
        else:
            # Add help text for faculty members
            self.fields['is_gold'].help_text = "Mark this as a Gold Seed to offer tokens for completion"
            self.fields['token_reward'].help_text = "Number of tokens to award for completion"
            self.fields['gold_goal'].help_text = "How tokens will be awarded"
            self.fields['deadline'].help_text = "Deadline for submitting solutions"
            
            # If this is an existing project, format the deadline
            if instance and instance.deadline:
                self.initial['deadline'] = instance.deadline.strftime('%Y-%m-%dT%H:%M')

    def clean_github_link(self):
        """Validate GitHub repository URL"""
        url = self.cleaned_data['github_link']
        if url:  # Only validate if URL is provided
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
        
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
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
            if pdf_file.size > 10 * 1024 * 1024:
                raise ValidationError('PDF file must be smaller than 10MB')

            ext = os.path.splitext(pdf_file.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError('Only PDF files are allowed')

            file_type, encoding = mimetypes.guess_type(pdf_file.name)
            if file_type != 'application/pdf':
                raise ValidationError('Invalid PDF file')

        return pdf_file

    def clean_featured_image(self):
        """Validate and process featured image"""
        image = self.cleaned_data.get('featured_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file must be smaller than 5MB')

            try:
                img = Image.open(image)
                
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                if img.width > 2000 or img.height > 2000:
                    raise ValidationError('Image dimensions should not exceed 2000x2000 pixels')
                
                if img.width > 1200 or img.height > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='JPEG', quality=85, optimize=True)
                output.seek(0)
                
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
    """Form for adding comments to projects"""
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

# Add this class to forms.py

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
        model = UserProfile
        fields = [
            'avatar',
            'bio',
            'location',
            'website',
            'github_username',
            'linkedin_url',
            'title',
            'department',
            'research_interests',
            
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
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your LinkedIn URL'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return avatar

class RatingForm(forms.ModelForm):
    """Form for rating projects"""
    class Meta:
        model = Rating
        fields = ['score', 'review']

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
    query = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-clap_count', 'Most popular'),
            ('title', 'Alphabetical'),
        ]
    )

class AdvancedSearchForm(forms.Form):
    """Advanced search form"""
    query = forms.CharField(required=False)
    tags = forms.CharField(required=False)
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    min_claps = forms.IntegerField(required=False, min_value=0)
    has_github = forms.BooleanField(required=False)
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-clap_count', 'Most popular'),
            ('-comment_count', 'Most discussed'),
            ('title', 'Alphabetical'),
            ('-rating_avg', 'Highest rated')
        ]
    )


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

class ProjectForm(forms.ModelForm, FileValidationMixin):
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
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project in detail...'
            }),
            'github_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repository'
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
        url = self.cleaned_data['github_link']
        if url:  # Only validate if URL is provided
            if not url.startswith(('https://github.com/', 'http://github.com/')):
                raise ValidationError('Please enter a valid GitHub repository URL')
            
            try:
                URLValidator()(url)
            except ValidationError:
                raise ValidationError('Please enter a valid URL')
        
        return url

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            return ''
        
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        seen = set()
        unique_tags = [x for x in tag_list if not (x in seen or seen.add(x))]
        
        if len(unique_tags) > 5:
            raise ValidationError('Please enter no more than 5 unique tags')
        
        if any(len(tag) > 20 for tag in unique_tags):
            raise ValidationError('Each tag must be less than 20 characters')
        
        return ', '.join(unique_tags)

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            self.validate_file_size(pdf_file, 10)
            self.validate_file_type(pdf_file, ['application/pdf'])
        return pdf_file

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            self.validate_file_size(image, 5)
            img = self.validate_image(image)
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            if img.width > 1200 or img.height > 1200:
                output_size = (1200, 1200)
                img.thumbnail(output_size, Image.LANCZOS)
            
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            from django.core.files.uploadedfile import InMemoryUploadedFile
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{os.path.splitext(image.name)[0]}.jpg",
                'image/jpeg',
                output.tell(),
                None
            )
        return image

class CommentForm(forms.ModelForm, FileValidationMixin):
    """Form for adding comments to projects"""
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if len(content) < 10:
            raise ValidationError('Comment must be at least 10 characters long')
        if len(content) > 1000:
            raise ValidationError('Comment must be less than 1000 characters')
        return content

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            self.validate_file_size(image, 2)
            img = self.validate_image(image, 1000)
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            if img.width > 800 or img.height > 800:
                output_size = (800, 800)
                img.thumbnail(output_size, Image.LANCZOS)
            
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            from django.core.files.uploadedfile import InMemoryUploadedFile
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{os.path.splitext(image.name)[0]}.jpg",
                'image/jpeg',
                output.tell(),
                None
            )
        return image

class UserProfileForm(forms.ModelForm, FileValidationMixin):
    """Form for user profile management"""
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'location', 'website', 'github_username',
            'linkedin_url', 'avatar', 'email_on_comment',
            'email_on_follow', 'email_on_clap', 'email_on_bookmark'
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
                'placeholder': 'https://yourwebsite.com'
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your GitHub username'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/your-profile'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            self.validate_file_size(avatar, 5)
            img = self.validate_image(avatar)
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
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
        return avatar

class RatingForm(forms.ModelForm):
    """Form for rating projects"""
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.Select(attrs={
                'class': 'form-select'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your review here...'
            })
        }

class BookmarkForm(forms.ModelForm):
    """Form for managing bookmarks"""
    class Meta:
        model = Bookmark
        fields = ['project']
        widgets = {
            'project': forms.HiddenInput()
        }

class NotificationSettingsForm(forms.Form):
    """Form for notification preferences"""
    email_on_comment = forms.BooleanField(
        required=False,
        label='Email me when someone comments on my projects'
    )
    email_on_follow = forms.BooleanField(
        required=False,
        label='Email me when someone follows me'
    )
    email_on_clap = forms.BooleanField(
        required=False,
        label='Email me when someone clap_count for my projects'
    )
    email_on_bookmark = forms.BooleanField(
        required=False,
        label='Email me when someone bookmarks my projects'
    )

class ProjectSearchForm(forms.Form):
    """Form for project search and filtering"""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search seeds...'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by tags (comma separated)'
        })
    )
    
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest first'),
            ('created_at', 'Oldest first'),
            ('-clap_count', 'Most popular'),
            ('title', 'Alphabetical'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

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
            ('-clap_count', 'Most popular'),
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
    

# In forms.py
from django import forms
from .models import Project, Comment
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
import os

class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects."""
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
        fields = ['title', 'description', 'github_link', 'tags', 'youtube_url', 
                 'pdf_file', 'featured_image', 'additional_files']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only show gold seed fields to faculty members
        if self.user and self.user.groups.filter(name='Faculty').exists():
            self.fields['is_gold'] = forms.BooleanField(required=False)
            self.fields['token_reward'] = forms.IntegerField(required=False)
            self.fields['gold_goal'] = forms.ChoiceField(
                choices=[
                    ('all', 'All Complete'),
                    ('first', 'First to Complete'),
                    ('best', 'Best Solution')
                ],
                required=False
            )
            self.fields['deadline'] = forms.DateTimeField(
                required=False,
                widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
            )
        
    def clean_youtube_url(self):
        url = self.cleaned_data.get('youtube_url')
        if url:
            from .models import validate_youtube_url
            validate_youtube_url(url)
        return url

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file and pdf_file.size > 10 * 1024 * 1024:  # 10MB limit
            raise ValidationError('PDF file must be smaller than 10MB')
        return pdf_file

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image file must be smaller than 5MB')
            try:
                img = Image.open(image)
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Resize if needed
                if img.width > 1200 or img.height > 1200:
                    output_size = (1200, 1200)
                    img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='JPEG', quality=85)
                output.seek(0)
                
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

class ExtendedUserCreationForm(UserCreationForm):
    talent_type = forms.ChoiceField(
        choices=TALENT_TYPES,
        required=True,
        label='Select Your Talent Type',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'talent_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                talent_type=self.cleaned_data['talent_type']
            )
        return user

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['content', 'files', 'github_link']

from django import forms
from .models import Team, TeamDiscussion, TeamComment, TeamMembership

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'tags', 'team_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter team name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your team and its goals'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., AI, Healthcare, Research)'
            }),
            'team_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.instance.pk:
            if Team.objects.exclude(pk=self.instance.pk).filter(name__iexact=name).exists():
                raise forms.ValidationError('A team with this name already exists.')
        else:
            if Team.objects.filter(name__iexact=name).exists():
                raise forms.ValidationError('A team with this name already exists.')
        return name


class TeamDiscussionForm(forms.ModelForm):
    """Form for creating and editing team discussions"""
    class Meta:
        model = TeamDiscussion
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Discussion title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Start your discussion here...'
            })
        }

class TeamCommentForm(forms.ModelForm):
    """Form for adding comments to discussions"""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Write your comment here...'
        })
    )
    class Meta:
        model = TeamComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }


class TeamMembershipForm(forms.ModelForm):
    class Meta:
        model = TeamMembership
        fields = ['role', 'is_approved']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow certain role choices based on permissions
        user = kwargs.get('initial', {}).get('user')
        if user and not user.is_staff:
            self.fields['role'].choices = [
                ('member', 'Member'),
                ('moderator', 'Moderator')
            ]

class TeamNotificationSettingsForm(forms.Form):
    email_notifications = forms.BooleanField(required=False)
    in_app_notifications = forms.BooleanField(required=False)

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'tags', 'team_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={
                'placeholder': 'Enter tags separated by commas'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Team.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('A team with this name already exists.')
        return name
    
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            # Split tags by comma and clean them
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            # Rejoin cleaned tags
            return ', '.join(tag_list)
        return tags

# forms.py additions




class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = ['name', 'logo', 'description', 'website']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter startup name'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your startup'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            })
        }

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            if logo.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            return logo
        return None

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your product'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            })
        }

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'description', 'image', 'url', 'github_url', 'documentation_url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tool name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your tool'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/...'
            }),
            'documentation_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            })
        }

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'description', 'file', 'format', 'license']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter dataset name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your dataset'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.zip,.csv,.json,.txt'
            }),
            'format': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CSV, JSON, etc.'
            }),
            'license': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., MIT, Apache, etc.'
            })
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 50 * 1024 * 1024:  # 50MB limit
                raise forms.ValidationError("File too large ( > 50MB )")
        return file

class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['name', 'logo', 'level', 'website', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization name'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your organization'
            })
        }

class VirtualMemberForm(forms.ModelForm):
    class Meta:
        model = VirtualMember
        fields = ['name', 'avatar', 'specialty', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Virtual member name'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'specialty': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area of expertise'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe this virtual member'
            })
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'type',
            'name',
            'email',
            'organization',
            'level',
            'message',
            'attachment'
        ]
        widgets = {
            'type': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization name'
            }),
            'level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us about yourself or your organization'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields optional
        self.fields['organization'].required = False
        self.fields['level'].required = False
        self.fields['attachment'].required = False

# Contents from: .\management\__init__.py


# Contents from: .\management\commands\__init__.py


# Contents from: .\management\commands\create_team_analytics.py
# projects/management/commands/create_team_analytics.py

from django.core.management.base import BaseCommand
from projects.models import Team, TeamAnalytics

class Command(BaseCommand):
    help = 'Creates analytics entries for existing teams'

    def handle(self, *args, **options):
        teams = Team.objects.all()
        created_count = 0
        
        for team in teams:
            analytics, created = TeamAnalytics.objects.get_or_create(
                team=team,
                defaults={
                    'total_discussions': team.discussions.count(),
                    'total_comments': sum(d.comments.count() for d in team.discussions.all()),
                    'active_members': team.memberships.filter(is_approved=True).count()
                }
            )
            if created:
                created_count += 1
                
        self.stdout.write(
            self.style.SUCCESS(f"Created analytics for {created_count} teams")
        )

# Contents from: .\management\commands\debug_teams.py
# projects/management/commands/debug_teams.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models import (
    Team, 
    TeamMembership, 
    KHCCBrain,
    UserProfile
)

class Command(BaseCommand):
    help = 'Debug teams and KHCC Brain membership'

    def handle(self, *args, **options):
        self.stdout.write("\n=== Starting Debug Process ===")
        
        # 1. Check KHCC Brain user
        self.stdout.write("\n=== Checking KHCC Brain User ===")
        KHCC_brain_user = None
        try:
            KHCC_brain = KHCCBrain.objects.first()
            if not KHCC_brain:
                KHCC_brain = KHCCBrain.objects.create()
                self.stdout.write("Created new KHCC Brain instance")
            
            KHCC_brain_user = User.objects.filter(username='KHCC_brain').first()
            if not KHCC_brain_user:
                KHCC_brain_user = User.objects.create_user(
                    username='KHCC_brain',
                    email='KHCC_brain@khcc.jo',
                    first_name='KHCC',
                    last_name='Brain'
                )
                UserProfile.objects.get_or_create(
                    user=KHCC_brain_user,
                    defaults={
                        'bio': "AI Research Assistant",
                        'title': "AI Assistant",
                        'department': "AI Lab"
                    }
                )
                self.stdout.write("Created KHCC Brain user")
            
            self.stdout.write(self.style.SUCCESS(
                f"✓ KHCC Brain user exists: {KHCC_brain_user.username}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"✗ Error with KHCC Brain user: {str(e)}"
            ))

        # 2. List all teams
        self.stdout.write("\n=== Listing All Teams ===")
        teams = Team.objects.all()
        if teams.exists():
            for team in teams:
                self.stdout.write(f"Team: {team.name}")
                self.stdout.write(f"- Created by: {team.founder.username}")
                self.stdout.write("- Members:")
                for membership in team.memberships.all():
                    self.stdout.write(f"  * {membership.user.username} (Role: {membership.role})")
        else:
            self.stdout.write(self.style.WARNING("No teams found in database"))

        # 3. Check team roles
        self.stdout.write("\n=== Available Team Roles ===")
        team_roles = [
            choice[0] for choice in TeamMembership._meta.get_field('role').choices
        ]
        self.stdout.write(f"Available roles: {team_roles}")

        # 4. Check memberships and join teams
        if KHCC_brain_user:
            self.stdout.write("\n=== Current KHCC Brain Memberships ===")
            current_memberships = TeamMembership.objects.filter(user=KHCC_brain_user)
            if current_memberships.exists():
                for membership in current_memberships:
                    self.stdout.write(f"Member of: {membership.team.name} (Role: {membership.role})")
            else:
                self.stdout.write("No current memberships")

            self.stdout.write("\n=== Attempting to Join New Teams ===")
            new_teams = Team.objects.exclude(memberships__user=KHCC_brain_user)
            for team in new_teams:
                try:
                    # Use 'member' role as it's likely to exist in your choices
                    membership = TeamMembership.objects.create(
                        team=team,
                        user=KHCC_brain_user,
                        role='member',  # Using 'member' as a safe default
                        is_approved=True
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Successfully joined team: {team.name}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"✗ Error joining team {team.name}: {str(e)}"
                    ))

        self.stdout.write("\n=== Debug Process Complete ===")

# Contents from: .\management\commands\join_teams.py
# projects/management/commands/join_teams.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import Team, TeamMembership, KHCCBrain

class Command(BaseCommand):
    help = 'Makes KHCC Brain join all teams it is not part of'

    def handle(self, *args, **options):# projects/management/commands/debug_teams.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import Team, TeamMembership, KHCCBrain
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Debug teams and KHCC Brain membership'

    def handle(self, *args, **options):
        # 1. Check KHCC Brain user
        self.stdout.write("\n=== Checking KHCC Brain User ===")
        try:
            KHCC_brain_user = KHCCBrain.get_user()
            self.stdout.write(self.style.SUCCESS(
                f"✓ KHCC Brain user exists: {KHCC_brain_user.username}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"✗ Error with KHCC Brain user: {str(e)}"
            ))

        # 2. List all teams
        self.stdout.write("\n=== Listing All Teams ===")
        teams = Team.objects.all()
        if teams.exists():
            for team in teams:
                self.stdout.write(f"Team: {team.name}")
                self.stdout.write(f"- Created by: {team.founder.username}")
                self.stdout.write("- Members:")
                for membership in team.memberships.all():
                    self.stdout.write(f"  * {membership.user.username} (Role: {membership.role})")
        else:
            self.stdout.write(self.style.WARNING("No teams found in database"))

        # 3. Check memberships
        self.stdout.write("\n=== Checking Team Memberships ===")
        if KHCC_brain_user:
            memberships = TeamMembership.objects.filter(user=KHCC_brain_user)
            if memberships.exists():
                self.stdout.write("KHCC Brain is member of:")
                for membership in memberships:
                    self.stdout.write(f"- {membership.team.name} (Role: {membership.role})")
            else:
                self.stdout.write(self.style.WARNING("KHCC Brain is not a member of any teams"))

        # 4. Try to join teams
        self.stdout.write("\n=== Attempting to Join Teams ===")
        if KHCC_brain_user:
            new_teams = Team.objects.exclude(memberships__user=KHCC_brain_user)
            if new_teams.exists():
                for team in new_teams:
                    try:
                        membership, created = TeamMembership.objects.get_or_create(
                            team=team,
                            user=KHCC_brain_user,
                            defaults={
                                'role': 'ai_assistant',
                                'is_approved': True
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(
                                f"✓ Successfully joined team: {team.name}"
                            ))
                        else:
                            self.stdout.write(
                                f"Already a member of: {team.name}"
                            )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f"✗ Error joining team {team.name}: {str(e)}"
                        ))
            else:
                self.stdout.write("No new teams to join")

        # 5. Print team role choices
        self.stdout.write("\n=== Available Team Roles ===")
        try:
            team_roles = [role[0] for role in TeamMembership._meta.get_field('role').choices]
            self.stdout.write(f"Team roles: {team_roles}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error getting team roles: {str(e)}"))

        # 6. Check if ai_assistant is a valid role
        self.stdout.write("\n=== Checking Role Configuration ===")
        try:
            from projects.models import TeamMembership
            role_choices = dict(TeamMembership._meta.get_field('role').choices)
            self.stdout.write(f"Available roles: {list(role_choices.keys())}")
            if 'ai_assistant' not in role_choices:
                self.stdout.write(self.style.WARNING(
                    "'ai_assistant' is not in the available roles. Using 'member' instead."
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error checking roles: {str(e)}"))
        try:
            # Get KHCC Brain user
            KHCC_brain_user = KHCCBrain.get_user()
            self.stdout.write(f"Found KHCC Brain user: {KHCC_brain_user.username}")

            # Get all teams
            all_teams = Team.objects.all()
            self.stdout.write(f"Found {all_teams.count()} total teams")

            # Get teams KHCC Brain hasn't joined
            new_teams = Team.objects.exclude(
                memberships__user=KHCC_brain_user
            )
            self.stdout.write(f"Found {new_teams.count()} teams to join")

            # Join each team
            for team in new_teams:
                try:
                    membership = TeamMembership.objects.create(
                        team=team,
                        user=KHCC_brain_user,
                        role='ai_assistant',
                        is_approved=True
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully joined team: {team.name}")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error joining team {team.name}: {str(e)}")
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error: {str(e)}")
            )

# Contents from: .\management\commands\run_khcc_brain.py
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

# Contents from: .\management\commands\send_welcome_messages.py
# projects/management/commands/send_welcome_messages.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import (
    Team, 
    TeamMembership, 
    KHCCBrain,
    TeamDiscussion,
    User
)

class Command(BaseCommand):
    help = 'Sends welcome messages to teams KHCC Brain has joined'

    def handle(self, *args, **options):
        self.stdout.write("\n=== Starting Welcome Messages Process ===")
        
        try:
            # Get KHCC Brain user
            KHCC_brain_user = User.objects.get(username='KHCC_brain')
            
            # Get teams where KHCC Brain is a member
            memberships = TeamMembership.objects.filter(user=KHCC_brain_user)
            
            for membership in memberships:
                team = membership.team
                
                # Check if welcome message already exists
                existing_welcome = TeamDiscussion.objects.filter(
                    team=team,
                    author=KHCC_brain_user,
                    title="KHCC Brain Introduction"
                ).exists()
                
                if not existing_welcome:
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
                        author=KHCC_brain_user,
                        title="KHCC Brain Introduction",
                        content=welcome_message
                    )
                    
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Posted welcome message to team: {team.name}"
                    ))
                else:
                    self.stdout.write(f"Welcome message already exists for team: {team.name}")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
            
        self.stdout.write("\n=== Welcome Messages Process Complete ===")

# Contents from: .\middleware.py
# projects/middleware.py

from django.conf import settings
from .models.analytics import PageVisit
import re

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_paths = getattr(settings, 'PAGE_ANALYTICS', {}).get('EXCLUDE_PATHS', [])
        self.exclude_patterns = [re.compile(pattern) for pattern in self.exclude_paths]

    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip tracking for excluded paths
        if any(pattern.match(request.path) for pattern in self.exclude_patterns):
            return response

        # Skip tracking for excluded user groups
        if request.user.is_authenticated:
            excluded_groups = getattr(settings, 'PAGE_ANALYTICS', {}).get('EXCLUDE_USER_GROUPS', [])
            if any(group.name in excluded_groups for group in request.user.groups.all()):
                return response

        # Create page visit record
        PageVisit.objects.create(
            path=request.path,
            user=request.user if request.user.is_authenticated else None,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referrer=request.META.get('HTTP_REFERER', ''),
            device_type=self.get_device_type(request),
            browser=self.get_browser(request)
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get_device_type(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'mobile' in user_agent:
            return 'mobile'
        elif 'tablet' in user_agent:
            return 'tablet'
        return 'desktop'

    def get_browser(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'chrome' in user_agent:
            return 'chrome'
        elif 'firefox' in user_agent:
            return 'firefox'
        elif 'safari' in user_agent:
            return 'safari'
        elif 'edge' in user_agent:
            return 'edge'
        return 'other'

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


# Contents from: .\migrations\0010_userprofile_email_on_bookmark_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0009_follow"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email_on_bookmark",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email_on_clap",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email_on_comment",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email_on_follow",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="twitter_username",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]


# Contents from: .\migrations\0011_alter_project_github_link.py
# Generated by Django 5.1.3 on 2024-11-18 15:11

import django.core.validators
import projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0010_userprofile_email_on_bookmark_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="github_link",
            field=models.URLField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.URLValidator(),
                    projects.models.validate_github_url,
                ],
            ),
        ),
    ]


# Contents from: .\migrations\0012_alter_project_slug.py
# Generated by Django 5.1.3 on 2024-11-18 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0011_alter_project_github_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]


# Contents from: .\migrations\0013_project_total_ratings.py
# Generated by Django 5.1.3 on 2024-11-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0012_alter_project_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="total_ratings",
            field=models.PositiveIntegerField(default=0),
        ),
    ]


# Contents from: .\migrations\0014_rename_total_ratings_project_rating_count_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0013_project_total_ratings"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="total_ratings",
            new_name="rating_count",
        ),
        migrations.AddField(
            model_name="project",
            name="rating_total",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]


# Contents from: .\migrations\0015_userprofile_department_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0014_rename_total_ratings_project_rating_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="department",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="research_interests",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="title",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]


# Contents from: .\migrations\0016_rename_claps_project_clap_count_alter_clap_project_and_more.py
# Generated by Django 5.1.3 on 2024-11-18 17:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0015_userprofile_department_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="claps",
            new_name="clap_count",
        ),
        migrations.AlterField(
            model_name="clap",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="claps",
                to="projects.project",
            ),
        ),
        migrations.AlterField(
            model_name="clap",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_claps",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]


# Contents from: .\migrations\0017_comment_clap_count_commentclap.py
# Generated by Django 5.1.3 on 2024-11-19 07:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_rename_claps_project_clap_count_alter_clap_project_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='clap_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='CommentClap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claps', to='projects.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_claps', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('comment', 'user')},
            },
        ),
    ]


# Contents from: .\migrations\0018_project_youtube_url.py
# Generated by Django 5.1.3 on 2024-11-19 15:40

import projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0017_comment_clap_count_commentclap"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="youtube_url",
            field=models.URLField(
                blank=True,
                help_text="Link to a YouTube video for your project",
                null=True,
                validators=[projects.models.validate_youtube_url],
            ),
        ),
    ]


# Contents from: .\migrations\0019_userprofile_talent_type.py
# Generated by Django 5.1.3 on 2024-11-19 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0018_project_youtube_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="talent_type",
            field=models.CharField(
                choices=[
                    ("ai", "AI Talent"),
                    ("healthcare", "Healthcare Talent"),
                    ("quality", "Quality Talent"),
                    ("engineering", "Engineering Talent"),
                    ("planning", "Planning Talent"),
                    ("design", "Design Talent"),
                    ("lab", "Lab Talent"),
                    ("extra", "Extra Talent"),
                ],
                default="ai",
                max_length=20,
                verbose_name="Talent Type",
            ),
        ),
    ]


# Contents from: .\migrations\0020_remove_userprofile_talent_type.py
# Generated by Django 5.1.3 on 2024-11-19 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0019_userprofile_talent_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="talent_type",
        ),
    ]


# Contents from: .\migrations\0021_userprofile_talent_type.py
# Generated by Django 5.1.3 on 2024-11-19 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0020_remove_userprofile_talent_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="talent_type",
            field=models.CharField(
                choices=[
                    ("ai", "AI Talent"),
                    ("healthcare", "Healthcare Talent"),
                    ("quality", "Quality Talent"),
                    ("engineering", "Engineering Talent"),
                    ("planner", "Planner Talent"),
                    ("design", "Design Talent"),
                    ("lab", "Lab Talent"),
                ],
                default="ai",
                max_length=20,
                verbose_name="Talent Type",
            ),
        ),
    ]


# Contents from: .\migrations\0022_alter_userprofile_talent_type.py
# Generated by Django 5.1.3 on 2024-11-19 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0021_userprofile_talent_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="talent_type",
            field=models.CharField(
                choices=[
                    ("ai", "AI Talent"),
                    ("healthcare", "Healthcare Talent"),
                    ("quality", "Quality Talent"),
                    ("engineering", "Engineering Talent"),
                    ("planning", "Planning Talent"),
                    ("design", "Design Talent"),
                    ("lab", "Lab Talent"),
                    ("extra", "Extra Talent"),
                ],
                default="ai",
                max_length=20,
                verbose_name="Talent Type",
            ),
        ),
    ]


# Contents from: .\migrations\0023_project_deadline_project_is_completed_and_more.py
# Generated by Django 5.1.3 on 2024-11-19 17:39

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0022_alter_userprofile_talent_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="project",
            name="is_gold",
            field=models.BooleanField(
                default=False, help_text="Mark this as a Gold Seed (Faculty only)"
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="reward_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("all", "All Complete"),
                    ("first", "First to Complete"),
                    ("best", "Best Solution"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="token_reward",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Number of tokens awarded for completion",
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="Solution",
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
                (
                    "files",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="solutions/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=[
                                    "pdf",
                                    "doc",
                                    "docx",
                                    "zip",
                                    "py",
                                    "ipynb",
                                    "txt",
                                ]
                            )
                        ],
                    ),
                ),
                ("github_link", models.URLField(blank=True, null=True)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("is_approved", models.BooleanField(default=False)),
                ("faculty_feedback", models.TextField(blank=True)),
                ("tokens_awarded", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="solutions",
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


# Contents from: .\migrations\0024_rename_reward_type_project_gold_goal.py
# Generated by Django 5.1.3 on 2024-11-19 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0023_project_deadline_project_is_completed_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="reward_type",
            new_name="gold_goal",
        ),
    ]


# Contents from: .\migrations\0025_team_teamanalytics_teamdiscussion_teamcomment_and_more.py
# Generated by Django 5.1.3 on 2024-11-19 19:23

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0024_rename_reward_type_project_gold_goal"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                ("description", models.TextField()),
                (
                    "tags",
                    models.CharField(
                        blank=True,
                        help_text="Enter tags separated by commas",
                        max_length=200,
                    ),
                ),
                (
                    "max_members",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MaxValueValidator(50)],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "founder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="founded_teams",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamAnalytics",
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
                ("total_discussions", models.PositiveIntegerField(default=0)),
                ("total_comments", models.PositiveIntegerField(default=0)),
                ("active_members", models.PositiveIntegerField(default=0)),
                ("last_activity", models.DateTimeField(blank=True, null=True)),
                ("discussions_this_week", models.PositiveIntegerField(default=0)),
                ("comments_this_week", models.PositiveIntegerField(default=0)),
                ("discussions_this_month", models.PositiveIntegerField(default=0)),
                ("comments_this_month", models.PositiveIntegerField(default=0)),
                (
                    "team",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analytics",
                        to="projects.team",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Team analytics",
            },
        ),
        migrations.CreateModel(
            name="TeamDiscussion",
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
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("pinned", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussions",
                        to="projects.team",
                    ),
                ),
            ],
            options={
                "ordering": ["-pinned", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="TeamComment",
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
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "discussion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="projects.teamdiscussion",
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="TeamMembership",
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
                    "role",
                    models.CharField(
                        choices=[
                            ("founder", "Team Founder"),
                            ("moderator", "Team Moderator"),
                            ("member", "Team Member"),
                        ],
                        default="member",
                        max_length=20,
                    ),
                ),
                ("is_approved", models.BooleanField(default=False)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("notification_preferences", models.JSONField(default=dict)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="projects.team",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["joined_at"],
                "unique_together": {("team", "user")},
            },
        ),
    ]


# Contents from: .\migrations\0026_alter_teammembership_options_and_more.py
# Generated by Django 5.1.3 on 2024-11-19 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0025_team_teamanalytics_teamdiscussion_teamcomment_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="teammembership",
            options={},
        ),
        migrations.RenameField(
            model_name="teammembership",
            old_name="joined_at",
            new_name="created_at",
        ),
        migrations.RemoveField(
            model_name="teammembership",
            name="notification_preferences",
        ),
        migrations.AddField(
            model_name="teammembership",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="teammembership",
            name="role",
            field=models.CharField(
                choices=[
                    ("founder", "Founder"),
                    ("moderator", "Moderator"),
                    ("member", "Member"),
                ],
                default="member",
                max_length=10,
            ),
        ),
    ]


# Contents from: .\migrations\0027_alter_team_options_remove_team_max_members_and_more.py
# Generated by Django 5.1.3 on 2024-11-19 19:45

import projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0026_alter_teammembership_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RemoveField(
            model_name="team",
            name="max_members",
        ),
        migrations.AddField(
            model_name="team",
            name="team_image",
            field=models.ImageField(
                blank=True,
                help_text="Upload a team profile image",
                null=True,
                upload_to=projects.models.team_image_upload_path,
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="team",
            name="slug",
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]


# Contents from: .\migrations\0028_dataset_product_sponsorship_tool_and_more.py
# Generated by Django 5.1.3 on 2024-11-21 03:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0027_alter_team_options_remove_team_max_members_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Dataset",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("file", models.FileField(upload_to="datasets/")),
                ("size", models.BigIntegerField()),
                ("format", models.CharField(max_length=50)),
                ("license", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("downloads", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="product_images/")),
                ("url", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Sponsorship",
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
                ("name", models.CharField(max_length=200)),
                ("logo", models.ImageField(upload_to="sponsor_logos/")),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("bronze", "Bronze"),
                            ("silver", "Silver"),
                            ("gold", "Gold"),
                            ("platinum", "Platinum"),
                        ],
                        max_length=20,
                    ),
                ),
                ("website", models.URLField()),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tool",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="tool_images/")),
                ("url", models.URLField()),
                ("github_url", models.URLField(blank=True)),
                ("documentation_url", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="generated_tags",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="project",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Application",
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
                    "type",
                    models.CharField(
                        choices=[
                            ("faculty", "Faculty"),
                            ("sponsor", "Sponsor"),
                            ("startup", "Startup"),
                            ("student", "Student"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "resume",
                    models.FileField(blank=True, null=True, upload_to="applications/"),
                ),
                ("cover_letter", models.TextField()),
                ("additional_info", models.JSONField(default=dict)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Startup",
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
                ("name", models.CharField(max_length=200)),
                ("logo", models.ImageField(upload_to="startup_logos/")),
                ("description", models.TextField()),
                ("website", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "founder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        related_name="startups", to="projects.product"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VirtualMember",
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
                ("name", models.CharField(max_length=100)),
                ("avatar", models.ImageField(upload_to="virtual_members/")),
                ("specialty", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "projects",
                    models.ManyToManyField(
                        related_name="virtual_team_members", to="projects.project"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="virtual_members",
            field=models.ManyToManyField(
                related_name="assigned_projects", to="projects.virtualmember"
            ),
        ),
    ]


# Contents from: .\migrations\0029_rename_resume_application_attachment_and_more.py
# Generated by Django 5.1.3 on 2024-11-21 04:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0028_dataset_product_sponsorship_tool_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="application",
            old_name="resume",
            new_name="attachment",
        ),
        migrations.RenameField(
            model_name="application",
            old_name="cover_letter",
            new_name="message",
        ),
        migrations.RemoveField(
            model_name="application",
            name="additional_info",
        ),
        migrations.RemoveField(
            model_name="application",
            name="status",
        ),
        migrations.RemoveField(
            model_name="application",
            name="type",
        ),
        migrations.RemoveField(
            model_name="application",
            name="user",
        ),
        migrations.AddField(
            model_name="application",
            name="email",
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="application",
            name="level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("bronze", "Bronze"),
                    ("silver", "Silver"),
                    ("gold", "Gold"),
                    ("platinum", "Platinum"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="name",
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="application",
            name="organization",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]


# Contents from: .\migrations\0030_application_additional_info_application_cover_letter_and_more.py
# Generated by Django 5.1.3 on 2024-11-21 04:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0029_rename_resume_application_attachment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="additional_info",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="application",
            name="cover_letter",
            field=models.FileField(
                blank=True, null=True, upload_to="applications/cover_letters/"
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="resume",
            field=models.FileField(
                blank=True, null=True, upload_to="applications/resumes/"
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="type",
            field=models.CharField(
                choices=[("sponsor", "Sponsor"), ("team", "Team Member")],
                default=django.utils.timezone.now,
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="application",
            name="attachment",
            field=models.FileField(
                blank=True, null=True, upload_to="applications/attachments/"
            ),
        ),
    ]


# Contents from: .\migrations\0031_alter_application_options_and_more.py
# Generated by Django 5.1.3 on 2024-11-21 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "projects",
            "0030_application_additional_info_application_cover_letter_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="application",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RemoveField(
            model_name="application",
            name="additional_info",
        ),
        migrations.RemoveField(
            model_name="application",
            name="cover_letter",
        ),
        migrations.RemoveField(
            model_name="application",
            name="resume",
        ),
        migrations.AlterField(
            model_name="application",
            name="attachment",
            field=models.FileField(
                blank=True,
                help_text="PDF format preferred, max 10MB",
                null=True,
                upload_to="applications/",
            ),
        ),
        migrations.AlterField(
            model_name="application",
            name="message",
            field=models.TextField(
                help_text="Tell us about yourself or your organization"
            ),
        ),
    ]


# Contents from: .\migrations\0032_khccbrain.py
# Generated by Django 5.1.3 on 2024-11-21 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0031_alter_application_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="KHCCBrain",
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
                ("last_active", models.DateTimeField(auto_now=True)),
                ("total_comments", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "KHCC Brain",
                "verbose_name_plural": "KHCC Brain Instances",
            },
        ),
    ]


# Contents from: .\migrations\0033_khccbrain_description_khccbrain_name.py
# Generated by Django 5.1.3 on 2024-11-22 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0032_khccbrain"),
    ]

    operations = [
        migrations.AddField(
            model_name="khccbrain",
            name="description",
            field=models.CharField(
                default="AI Research Assistant & Team Mentor", max_length=100
            ),
        ),
        migrations.AddField(
            model_name="khccbrain",
            name="name",
            field=models.CharField(default="KHCC Brain", max_length=50),
        ),
    ]


# Contents from: .\migrations\0034_teamdiscussion_views.py
# Generated by Django 5.1.3 on 2024-11-22 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0033_khccbrain_description_khccbrain_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="teamdiscussion",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]


# Contents from: .\migrations\0035_teammembership_receive_notifications_and_more.py
# Generated by Django 5.1.3 on 2024-11-22 06:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0034_teamdiscussion_views"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="teammembership",
            name="receive_notifications",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="teammembership",
            name="role",
            field=models.CharField(
                choices=[
                    ("member", "Member"),
                    ("moderator", "Moderator"),
                    ("founder", "Founder"),
                ],
                default="member",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="teammembership",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
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
            You are KHCC Brain, an AI research assistant at KHCC.AI. Analyze this project and provide encouraging feedback.
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

# Contents from: .\models\analytics.py
# projects/models/analytics.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PageVisit(models.Model):
    path = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['path', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]

class EventTracker(models.Model):
    EVENT_TYPES = [
        ('view', 'Page View'),
        ('click', 'Click'),
        ('scroll', 'Scroll'),
        ('clap', 'Clap'),
        ('comment', 'Comment'),
        ('bookmark', 'Bookmark'),
    ]

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    target = models.CharField(max_length=100, blank=True)  # e.g., button id, element class
    metadata = models.JSONField(default=dict, blank=True)  # Additional event data

    class Meta:
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]

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

# Contents from: .\services\__init__.py
# projects/services/__init__.py
from .openai_service import OpenAITaggingService

__all__ = ['OpenAITaggingService']

# Contents from: .\services\openai_service.py
# projects/services/openai_service.py
from django.conf import settings
from openai import OpenAI

class OpenAITaggingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_tags(self, title: str, description: str) -> list[str]:
        """
        Generate tags for a project using OpenAI's API
        
        Args:
            title: Project title
            description: Project description
            
        Returns:
            List of generated tags
        """
        try:
            prompt = f"""
            Based on the following project title and description, generate up to 5 relevant tags.
            Format the response as a comma-separated list of lowercase tags.
            
            Title: {title}
            Description: {description}
            
            Tags should be:
            - Relevant to AI, machine learning, and data science
            - Single words or short phrases (max 2-3 words)
            - All lowercase
            - No special characters
            - No hashtags
            
            Example format: machine learning, nlp, computer vision, tensorflow, data analysis
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates relevant tags for AI and machine learning projects."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            # Extract tags from response
            tags = response.choices[0].message.content.strip()
            return tags
            
        except Exception as e:
            print(f"Error generating tags: {str(e)}")
            return ""

# Contents from: .\signals.py
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

# Contents from: .\templatetags\__init__.py


# Contents from: .\templatetags\analytics_tags.py
# projects/templatetags/analytics_tags.py

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('analytics/google_analytics.html')
def google_analytics():
    """
    Renders Google Analytics tracking code if GOOGLE_ANALYTICS_ID is set
    """
    return {
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
        'debug': settings.DEBUG
    }

# Contents from: .\templatetags\custom_filters.py
# projects/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by the given delimiter"""
    return value.split(arg)

# Contents from: .\templatetags\project_tags.py
# projects/templatetags/project_tags.py

from django import template
from django.db.models import Q
from ..models import Project

register = template.Library()

@register.simple_tag
def get_similar_projects(project):
    """Returns similar projects based on tags"""
    if not project.tags:
        return Project.objects.exclude(id=project.id)[:3]
    
    tags = [tag.strip() for tag in project.tags.split(',')]
    similar_projects = Project.objects.filter(
        tags__icontains=tags[0]
    ).exclude(id=project.id)
    
    for tag in tags[1:]:
        similar_projects = similar_projects | Project.objects.filter(
            tags__icontains=tag
        ).exclude(id=project.id)
    
    return similar_projects.distinct()[:3]

# Contents from: .\templatetags\query_tags.py
# templatetags/query_tags.py

from django import template
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag
def query_transform(request_get, param_name, value, action='add'):
    """
    Transform query parameters while preserving other parameters
    """
    updated = request_get.copy()
    
    if action == 'remove':
        # Remove a specific value from a comma-separated list
        current_values = updated.get(param_name, '').split(',')
        current_values = [v for v in current_values if v and v != value]
        if current_values:
            updated[param_name] = ','.join(current_values)
        else:
            updated.pop(param_name, None)
    else:
        # Add or replace value
        if value:
            updated[param_name] = value
        else:
            updated.pop(param_name, None)
    
    return '?' + urlencode(updated)

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

# Contents from: .\templatetags\team_tags.py
from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits a string into a list on the given delimiter
    Usage: {{ value|split:"," }}
    """
    return [x.strip() for x in value.split(arg)]

# Contents from: .\templatetags\user_tags.py
from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def is_faculty(user):
    """Check if user is in the Faculty group"""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='Faculty').exists()

# Contents from: .\tests.py
from django.test import TestCase

# Create your tests here.


# Contents from: .\tests\team_tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Team, TeamMembership, TeamDiscussion, TeamComment
from datetime import timedelta
from django.utils import timezone

class TeamTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Description',
            founder=self.user,
            max_members=10
        )
        TeamMembership.objects.create(
            team=self.team,
            user=self.user,
            role='founder',
            is_approved=True
        )

    def test_team_creation(self):
        response = self.client.post(reverse('create_team'), {
            'name': 'New Team',
            'description': 'New Description',
            'max_members': 15
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name='New Team').exists())

    def test_team_join(self):
        new_user = User.objects.create_user('newuser', 'new@test.com', 'newpass')
        self.client.login(username='newuser', password='newpass')
        
        response = self.client.post(reverse('join_team', args=[self.team.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamMembership.objects.filter(
            team=self.team,
            user=new_user,
            is_approved=False
        ).exists())

    def test_discussion_creation(self):
        response = self.client.post(
            reverse('create_discussion', args=[self.team.slug]),
            {
                'title': 'Test Discussion',
                'content': 'Test Content'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamDiscussion.objects.filter(
            team=self.team,
            title='Test Discussion'
        ).exists())

    def test_analytics_updates(self):
        discussion = TeamDiscussion.objects.create(
            team=self.team,
            author=self.user,
            title='Test Discussion',
            content='Test Content'
        )
        
        analytics = self.team.analytics
        self.assertEqual(analytics.total_discussions, 1)
        self.assertEqual(analytics.discussions_this_week, 1)

        TeamComment.objects.create(
            discussion=discussion,
            author=self.user,
            content='Test Comment'
        )
        
        analytics.refresh_from_db()
        self.assertEqual(analytics.total_comments, 1)
        self.assertEqual(analytics.comments_this_week, 1)

    def test_notification_preferences(self):
        membership = TeamMembership.objects.get(team=self.team, user=self.user)
        membership.notification_preferences = {
            'email_notifications': False,
            'in_app_notifications': True
        }
        membership.save()
        
        membership.refresh_from_db()
        self.assertFalse(membership.notification_preferences['email_notifications'])
        self.assertTrue(membership.notification_preferences['in_app_notifications'])

    def test_member_permissions(self):
        regular_user = User.objects.create_user('regular', 'regular@test.com', 'pass')
        membership = TeamMembership.objects.create(
            team=self.team,
            user=regular_user,
            role='member',
            is_approved=True
        )
        
        self.client.login(username='regular', password='pass')
        
        # Try to access team settings (should be forbidden)
        response = self.client.get(reverse('team_settings', args=[self.team.slug]))
        self.assertEqual(response.status_code, 403)

        # Can create discussions
        response = self.client.post(
            reverse('create_discussion', args=[self.team.slug]),
            {'title': 'Member Discussion', 'content': 'Content'}
        )
        self.assertEqual(response.status_code, 302)

# Contents from: .\tests\team_tests_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Team, TeamMembership

class TeamAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Description',
            founder=self.user
        )
        TeamMembership.objects.create(
            team=self.team,
            user=self.user,
            role='founder',
            is_approved=True
        )

    def test_team_list_api(self):
        response = self.client.get(reverse('api_team_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_team_detail_api(self):
        response = self.client.get(reverse('api_team_detail', args=[self.team.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Team')

    def test_team_analytics_api(self):
        response = self.client.get(reverse('api_team_analytics', args=[self.team.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_discussions', response.data)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(reverse('api_team_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Contents from: .\urls.py
# urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'projects'

urlpatterns = [
    # Homepage and Project List
    path('', views.homepage, name='homepage'),
    path('projects/', views.project_list, name='project_list'),
    
    # Project Management
    path('submit/', views.submit_project, name='submit_project'),
    path('search/', views.search_projects, name='search_projects'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    
    # Project Detail & Actions
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:pk>/rate/', views.rate_project, name='rate_project'),
    path('project/<int:pk>/bookmark/', views.bookmark_project, name='bookmark_project'),
    path('project/<int:pk>/clap/', views.clap_project, name='clap_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    
    # Analytics
    path('project/<int:pk>/analytics/', views.ProjectAnalyticsView.as_view(), name='project_analytics'),
    path('project/<int:pk>/analytics/data/', views.analytics_data, name='analytics_data'),
    path('project/<int:pk>/analytics/export/csv/', views.export_analytics_csv, name='export_analytics_csv'),
    path('project/<int:pk>/analytics/export/pdf/', views.export_analytics_pdf, name='export_analytics_pdf'),
    
    # User Profiles
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/projects/', views.user_projects, name='user_projects'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    
# Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', 
         views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', 
         views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Comments
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/clap/', views.clap_comment, name='clap_comment'),
    
    # Startups
    path('startups/', views.StartupListView.as_view(), name='startup_list'),
    path('startups/create/', 
         login_required(views.StartupCreateView.as_view()), 
         name='create_startup'),
    
    # Tools
    path('tools/', views.ToolListView.as_view(), name='tool_list'),
    path('tools/create/', 
         login_required(views.ToolCreateView.as_view()), 
         name='create_tool'),
    
    # Datasets
    path('datasets/', views.DatasetListView.as_view(), name='dataset_list'),
    path('datasets/create/', 
         login_required(views.DatasetCreateView.as_view()), 
         name='create_dataset'),
    
    # Downloads
    path('project/<int:pk>/download/', views.download_project, name='download_project'),
    path('dataset/<int:pk>/download/', views.download_dataset, name='download_dataset'),
    
    # Sponsorships and Applications
    path('sponsorships/', views.SponsorshipListView.as_view(), name='sponsorship_list'),
    path('virtual-members/', views.VirtualMemberListView.as_view(), name='virtual_member_list'),
    path('apply/', login_required(views.ApplicationCreateView.as_view()), name='apply'),
    
    # Other pages
    path('faculty/', views.faculty_page, name='faculty_page'),
    path('careers/', views.careers_page, name='careers'),
    path('talents/', views.talents_page, name='talents'),
    path('help/', views.help_view, name='help'),
    
    path('api/projects/<int:pk>/generate-tags/', 
         views.generate_tags, 
         name='api_generate_tags'),
    
    path('api/projects/<int:project_pk>/add-virtual-member/', 
         views.add_virtual_member, 
         name='api_add_virtual_member'),
    
    path('api/projects/<int:project_pk>/remove-virtual-member/<int:member_pk>/',
         views.remove_virtual_member,
         name='api_remove_virtual_member'),
    
    path('api/projects/<int:pk>/analytics/', 
         views.project_analytics_api,  # Changed to match the view function name
         name='api_project_analytics'),
    
    # Solutions
    path('project/<int:pk>/submit-solution/', 
         views.submit_solution, name='submit_solution'),
    path('project/<int:project_pk>/solution/<int:solution_pk>/review/', 
         views.review_solution, name='review_solution'),
# Team Management
     path('teams/', views.team_list, name='team_list'),
     path('teams/create/', views.create_team, name='create_team'),
     path('teams/<slug:team_slug>/', views.team_detail, name='team_detail'),
     path('teams/<slug:team_slug>/edit/', views.edit_team, name='edit_team'),
     path('teams/<slug:team_slug>/delete/', views.delete_team, name='delete_team'),
     path('teams/<slug:team_slug>/join/', views.join_team, name='join_team'),
     path('teams/<slug:team_slug>/leave/', views.leave_team, name='leave_team'),
     path('teams/<slug:team_slug>/members/', views.team_members, name='team_members'),
     path('teams/<slug:team_slug>/members/<int:user_id>/promote/', views.promote_member, name='promote_member'),
     path('teams/<slug:team_slug>/members/<int:user_id>/remove/', views.remove_member, name='remove_member'),
    path('help/', views.help_view, name='help'),
    path('faq/', views.faq, name='faq'),
    
    # Team URLs
    path('team/<slug:team_slug>/discussions/', 
         views.team_discussions, 
         name='team_discussions'),
    path('team/<slug:team_slug>/discussions/<int:discussion_id>/', 
         views.discussion_detail, 
         name='discussion_detail'),
    path('team/<slug:team_slug>/discussions/<int:discussion_id>/delete/', 
         views.delete_discussion, 
         name='delete_discussion'),
    path('team/<slug:team_slug>/analytics/', 
         views.team_analytics, 
         name='team_analytics'),
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
    """Send email for a new notification if user has enabled that notification type"""
    recipient_profile = notification.recipient.profile
    
    # Check if user wants this type of email notification
    should_send = False
    
    if notification.notification_type == 'comment' and recipient_profile.email_on_comment:
        should_send = True
    elif notification.notification_type == 'follow' and recipient_profile.email_on_follow:
        should_send = True
    elif notification.notification_type == 'clap' and recipient_profile.email_on_clap:
        should_send = True
    elif notification.notification_type == 'bookmark' and recipient_profile.email_on_bookmark:
        should_send = True
    
    if should_send:
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

# Contents from: .\utils\team_emails.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_team_notification_email(user, team, notification_type, context=None):
    """Send email notifications for team activities"""
    if context is None:
        context = {}
    
    context.update({
        'user': user,
        'team': team,
        'site_url': settings.SITE_URL
    })
    
    templates = {
        'discussion': 'emails/team_discussion.html',
        'comment': 'emails/team_comment.html',
        'role_change': 'emails/team_role_change.html',
        'invitation': 'emails/team_invitation.html'
    }
    
    template = templates.get(notification_type)
    if not template:
        return
        
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    
    subject = f"New activity in {team.name} - {notification_type.title()}"
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

def send_team_invitation_email(user, team, inviter):
    """Send email for team invitation"""
    context = {
        'user': user,
        'team': team,
        'inviter': inviter,
        'site_url': settings.SITE_URL
    }
    
    html_message = render_to_string('emails/team_invitation.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        f"Invitation to join {team.name}",
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

def send_role_change_notification(user, team, new_role):
    """Send email for role changes"""
    context = {
        'user': user,
        'team': team,
        'new_role': new_role,
        'site_url': settings.SITE_URL
    }
    
    html_message = render_to_string('emails/team_role_change.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        f"Role update in {team.name}",
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )

# Contents from: .\views.py
from datetime import datetime, timedelta
from io import StringIO, BytesIO
import csv
import json
import os
import pytz
import zipfile

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.db.models import Count, Q, Avg, Sum, Case, When, F
from django.db import models
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from khcc_psut_ai_lab.constants import TALENT_TYPES, TALENT_DICT

from .filters.project_filters import ProjectFilter
from .forms import (
    ProjectForm, CommentForm, ProjectSearchForm, UserProfileForm,
    RatingForm, BookmarkForm, AdvancedSearchForm, ProfileForm, 
    NotificationSettingsForm, ExtendedUserCreationForm,
    SolutionForm, TeamForm, TeamDiscussionForm, TeamCommentForm, 
    TeamNotificationSettingsForm, StartupForm, ProductForm, ToolForm,
    DatasetForm, SponsorshipForm, VirtualMemberForm, ApplicationForm
)

from .models import (
    Project, Comment, Clap, UserProfile, Rating,
    Bookmark, ProjectAnalytics, Notification, Follow,
    CommentClap, Solution, Team, TeamMembership, 
    TeamDiscussion, TeamComment, TeamAnalytics,
    Sponsorship, Startup, Product, Tool, Dataset,
    VirtualMember, Application
)

from .serializers import ProjectSerializer, ProjectAnalyticsSerializer, ProjectAnalyticsSummarySerializer
from .utils.pdf import generate_analytics_pdf

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import os
import zipfile
from io import BytesIO

# DRF imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Import all models
from .models import (
    Project, Comment, UserProfile, Rating, Bookmark, 
    ProjectAnalytics, Notification, Follow, CommentClap,
    Solution, Startup, Product, Tool, Dataset,
    VirtualMember, Application, Sponsorship
)

# Import all forms
from .forms import (
    ProjectForm, CommentForm, UserProfileForm, RatingForm,
    BookmarkForm, AdvancedSearchForm, ProfileForm,
    NotificationSettingsForm, ExtendedUserCreationForm,
    SolutionForm, StartupForm, ProductForm, ToolForm,
    DatasetForm, SponsorshipForm, VirtualMemberForm,
    ApplicationForm
)

# Add these to your views.py file

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_virtual_member(request, project_pk):
    """Add a virtual member to a project"""
    project = get_object_or_404(Project, pk=project_pk)
    
    # Check permissions
    if project.author != request.user:
        return Response({
            "status": "error",
            "message": "Permission denied"
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        member_id = request.data.get('member_id')
        if not member_id:
            return Response({
                "status": "error",
                "message": "member_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        virtual_member = get_object_or_404(VirtualMember, pk=member_id)
        
        # Check if member is already added
        if virtual_member in project.virtual_members.all():
            return Response({
                "status": "error",
                "message": "Virtual member already added to this project"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Add virtual member to project
        project.virtual_members.add(virtual_member)
        
        return Response({
            "status": "success",
            "message": f"Added {virtual_member.name} to project",
            "member": {
                "id": virtual_member.id,
                "name": virtual_member.name,
                "specialty": virtual_member.specialty
            }
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_virtual_member(request, project_pk, member_pk):
    """Remove a virtual member from a project"""
    project = get_object_or_404(Project, pk=project_pk)
    
    # Check permissions
    if project.author != request.user:
        return Response({
            "status": "error",
            "message": "Permission denied"
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        virtual_member = get_object_or_404(VirtualMember, pk=member_pk)
        
        # Check if member is in project
        if virtual_member not in project.virtual_members.all():
            return Response({
                "status": "error",
                "message": "Virtual member not found in this project"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Remove virtual member from project
        project.virtual_members.remove(virtual_member)
        
        return Response({
            "status": "success",
            "message": f"Removed {virtual_member.name} from project"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# views.py

from django.conf import settings
import openai
from khcc_psut_ai_lab.constants import ALL_TAGS
from difflib import get_close_matches

def get_similar_tags(suggested_tag, valid_tags=ALL_TAGS, n=1, cutoff=0.6):
    """Find the closest matching valid tag"""
    matches = get_close_matches(suggested_tag.lower(), valid_tags, n=n, cutoff=cutoff)
    return matches[0] if matches else suggested_tag

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_tags(request, pk):
    """Generate tags for a project using OpenAI"""
    project = get_object_or_404(Project, pk=pk)
    
    # Check permissions
    if project.author != request.user:
        return Response({
            "status": "error",
            "message": "Permission denied"
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        # Set up OpenAI client
        openai.api_key = settings.OPENAI_API_KEY
        
        # Prepare the prompt
        prompt = f"""
        Please analyze the following project and suggest relevant tags from the predefined list.
        The tags should be highly relevant to AI and healthcare domains.
        
        Project Title: {project.title}
        Project Description: {project.description}
        
        Available Tags: {', '.join(ALL_TAGS)}
        
        Please suggest 3-5 most relevant tags from the available tags list above.
        Return only the tags in a comma-separated format.
        Prefer exact matches from the available tags, but suggest close alternatives if needed.
        """
        
        # Make API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a specialized AI trained to analyze healthcare and AI projects and assign relevant tags."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more focused responses
            max_tokens=100
        )
        
        # Extract suggested tags from response
        suggested_tags = response.choices[0].message['content'].strip().split(',')
        suggested_tags = [tag.strip().lower() for tag in suggested_tags]
        
        # Map suggested tags to valid tags
        final_tags = []
        for tag in suggested_tags:
            if tag in ALL_TAGS:
                final_tags.append(tag)
            else:
                # Find similar valid tag
                similar_tag = get_similar_tags(tag)
                if similar_tag:
                    final_tags.append(similar_tag)
        
        # Remove duplicates and limit to 5 tags
        final_tags = list(dict.fromkeys(final_tags))[:5]
        
        # Update project's generated tags
        project.generated_tags = ",".join(final_tags)
        project.save()
        
        return Response({
            "status": "success",
            "tags": final_tags,
            "message": "Tags generated successfully using AI"
        })
        
    except openai.error.OpenAIError as e:
        return Response({
            "status": "error",
            "message": f"OpenAI API error: {str(e)}"
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_analytics_api(request, pk):
    """Get project analytics data"""
    project = get_object_or_404(Project, pk=pk)
    
    # Check permissions
    if project.author != request.user and not request.user.is_staff:
        return Response({
            "status": "error",
            "message": "Permission denied"
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        analytics = project.analytics
        
        # Get time period from query params
        period = request.GET.get('period', 'all')  # all, week, month
        
        if period == 'week':
            start_date = timezone.now() - timedelta(days=7)
        elif period == 'month':
            start_date = timezone.now() - timedelta(days=30)
        else:
            start_date = None
            
        data = {
            "overview": {
                "views": analytics.view_count,
                "unique_visitors": analytics.unique_visitors,
                "github_clicks": analytics.github_clicks,
                "avg_time_spent": str(analytics.avg_time_spent),
            },
            "device_stats": {
                "desktop": analytics.desktop_visits,
                "mobile": analytics.mobile_visits,
                "tablet": analytics.tablet_visits
            },
            "browser_stats": {
                "chrome": analytics.chrome_visits,
                "firefox": analytics.firefox_visits,
                "safari": analytics.safari_visits,
                "edge": analytics.edge_visits,
                "other": analytics.other_browsers
            },
            "traffic_sources": {
                "direct": analytics.direct_traffic,
                "social": analytics.social_traffic,
                "search": analytics.search_traffic,
                "referral": analytics.referral_traffic
            },
            "engagement": {
                "comments": project.comments.count(),
                "claps": project.clap_count,
                "bookmarks": project.bookmarks.count(),
                "average_rating": project.average_rating
            }
        }
        
        # Add periodic stats if a period is specified
        if start_date:
            data["periodic_stats"] = {
                "views": analytics.get_views_for_period(start_date),
                "unique_visitors": analytics.get_unique_visitors_for_period(start_date),
                "github_clicks": analytics.get_github_clicks_for_period(start_date),
                "comments": project.comments.filter(created_at__gte=start_date).count(),
                "claps": Clap.objects.filter(project=project, created_at__gte=start_date).count()
            }
        
        return Response({
            "status": "success",
            "data": data
        })
        
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            entry['clap_count']
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
    """View for listing projects with filters"""
    projects = Project.objects.all().select_related('author', 'author__profile')
    
    # Get query parameters
    query = request.GET.get('query', '')
    category = request.GET.get('category', 'all')
    sort = request.GET.get('sort', '-created_at')
    selected_tags = request.GET.getlist('tags')

    # Get top 10 most used tags
    all_tags = Project.objects.values('tags') \
        .annotate(tag_count=Count('tags')) \
        .order_by('-tag_count')
    popular_tags = [tag['tags'] for tag in all_tags[:10] if tag['tags']]

    # Apply filters
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()

    if category != 'all':
        if category == 'featured':
            projects = projects.filter(is_featured=True)
        elif category == 'gold':
            projects = projects.filter(is_gold=True)
        elif category == 'latest':
            projects = projects.order_by('-created_at')
        elif category == 'popular':
            projects = projects.annotate(
                popularity=Count('claps') + Count('comments')
            ).order_by('-popularity')

    # Apply tag filters
    if selected_tags:
        for tag in selected_tags:
            projects = projects.filter(tags__icontains=tag)

    # Apply sorting
    if sort:
        if sort == '-clap_count':
            projects = projects.annotate(
                total_claps=Count('claps')  # Changed from clap_count to total_claps
            ).order_by('-total_claps')
        elif sort == '-rating_avg':
            projects = projects.annotate(
                rating_avg=Avg('ratings__rating')
            ).order_by('-rating_avg')
        else:
            projects = projects.order_by(sort)

    # Annotate with counts for display
    projects = projects.annotate(
        total_comments=Count('comments')  # Changed from comment_count
    )

    # Pagination
    paginator = Paginator(projects, 12)  # Show 12 projects per page
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'popular_tags': popular_tags,
        'selected_tags': selected_tags,
    }

    return render(request, 'projects/project_list.html', context)

@login_required
def submit_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            
            # Handle gold seed fields for faculty
            if request.user.groups.filter(name='Faculty').exists():
                project.is_gold = form.cleaned_data.get('is_gold', False)
                if project.is_gold:
                    project.token_reward = form.cleaned_data.get('token_reward')
                    project.gold_goal = form.cleaned_data.get('gold_goal')
                    project.deadline = form.cleaned_data.get('deadline')
            
            project.save()
            
            # Handle tags
            if form.cleaned_data['tags']:
                project.tags = form.cleaned_data['tags']
            
            messages.success(request, 'Project submitted successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(user=request.user)
    
    return render(request, 'projects/submit_project.html', {
        'form': form,
        'title': 'Submit Seed'
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    comments = project.comments.filter(parent=None).select_related('user').prefetch_related(
        'replies', 
        'claps',
        'replies__claps',
        'replies__user'
    )
    
    # Handle POST requests (new comments)
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            
            # Handle replies
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                    # Create notification for parent comment author
                    if parent_comment.user != request.user:
                        Notification.objects.create(
                            recipient=parent_comment.user,
                            sender=request.user,
                            project=project,
                            notification_type='comment',
                            message=f"{request.user.username} replied to your comment"
                        )
                except Comment.DoesNotExist:
                    messages.error(request, 'Parent comment not found.')
                    return redirect('projects:project_detail', pk=pk)
            
            comment.save()
            
            # Create notification for project author (only for top-level comments)
            if project.author != request.user and not parent_id:
                Notification.objects.create(
                    recipient=project.author,
                    sender=request.user,
                    project=project,
                    notification_type='comment',
                    message=f"{request.user.username} commented on your project"
                )
            
            messages.success(request, 'Comment added successfully!')
            return redirect('projects:project_detail', pk=pk)
        else:
            messages.error(request, 'Error posting comment. Please check your input.')
    else:
        form = CommentForm()
    
    # Check clap status for authenticated users
    if request.user.is_authenticated:
        # Check if user has clapped for the project
        project.user_has_clapped = project.claps.filter(user=request.user).exists()
        
        # Check if user has clapped for comments
        for comment in comments:
            comment.has_user_clapped = comment.claps.filter(user=request.user).exists()
            for reply in comment.replies.all():
                reply.has_user_clapped = reply.claps.filter(user=request.user).exists()
        
        # Get user's bookmark if it exists
        user_bookmark = project.bookmarks.filter(user=request.user).first()
    else:
        project.user_has_clapped = False
        user_bookmark = None

    # Get project statistics
    stats = {
        'view_count': project.analytics.view_count if hasattr(project, 'analytics') else 0,
        'clap_count': project.clap_count,
        'comment_count': project.comments.count(),
        'rating_count': project.rating_count,
        'avg_rating': project.average_rating,
    }
    
    context = {
        'project': project,
        'comments': comments,
        'comment_form': form,
        'featured_image_url': project.get_featured_image_url(),
        'pdf_url': project.get_pdf_url(),
        'rating_form': RatingForm(),
        'user_bookmark': user_bookmark,
        'stats': stats,

    }
    
    # Update view count
    if hasattr(project, 'analytics'):
        project.analytics.view_count += 1
        project.analytics.save()
    
    return render(request, 'projects/project_detail.html', context)

@login_required
def rate_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        score = request.POST.get('score')
        review = request.POST.get('review', '')
        
        try:
            score = int(score)
            if not (1 <= score <= 5):
                return JsonResponse({'status': 'error', 'message': 'Invalid rating'}, status=400)
                
            rating, created = Rating.objects.update_or_create(
                project=project,
                user=request.user,
                defaults={
                    'score': score,
                    'review': review
                }
            )
            
            # Update project rating stats
            project.update_rating_stats()
            
            # Create notification for project author if it's a new rating
            if created and project.author != request.user:
                Notification.objects.create(
                    recipient=project.author,
                    sender=request.user,
                    project=project,
                    notification_type='rating',
                    message=f"{request.user.username} rated your project"
                )
            
            return JsonResponse({
                'status': 'success',
                'rating': project.average_rating,
                'total_ratings': project.rating_count
            })
            
        except (ValueError, TypeError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

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
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('projects:user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'projects/edit_profile.html', {
        'form': form,
        'active_tab': 'profile'
    })

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    projects = Project.objects.filter(author=profile_user).order_by('-created_at')
    
    # Get follow status
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()
    
    # Get statistics and counts
    stats = {
        'followers_count': Follow.objects.filter(following=profile_user).count(),
        'following_count': Follow.objects.filter(follower=profile_user).count(),
        'projects_count': projects.count(),
        'total_claps': Project.objects.filter(author=profile_user).aggregate(
            total_claps=Sum('clap_count')
        )['total_claps'] or 0,
        'total_comments': Comment.objects.filter(user=profile_user).count(),
    }
    
    context = {
        'profile_user': profile_user,
        'projects': projects,
        'is_following': is_following,
        'stats': stats,
        'is_faculty': profile_user.groups.filter(name='Faculty').exists(),
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
    form_class = ExtendedUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please log in.')
        return response

def get_monthly_contributions():
    """Get users sorted by their contributions in the current month"""
    start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    return User.objects.annotate(
        monthly_projects=Count(
            'project',
            filter=Q(project__created_at__gte=start_of_month)
        ),
        monthly_comments=Count(
            'comment',
            filter=Q(comment__created_at__gte=start_of_month)
        ),
        monthly_claps=Count(
            'user_claps',
            filter=Q(user_claps__created_at__gte=start_of_month)
        ),
        # Calculate total directly in the same annotation
        total_contributions=Count(
            'project',
            filter=Q(project__created_at__gte=start_of_month)
        ) + Count(
            'comment',
            filter=Q(comment__created_at__gte=start_of_month)
        ) + Count(
            'user_claps',
            filter=Q(user_claps__created_at__gte=start_of_month)
        )
    ).order_by('-total_contributions')

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
            'clap_count': user.claps_received or 0,
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
    project = get_object_or_404(Project, pk=pk)
    
    # Check if user is author
    if project.author != request.user:
        messages.error(request, "You don't have permission to edit this project.")
        return redirect('projects:project_detail', pk=project.pk)
    
    if request.method == 'POST':
        form = ProjectForm(
            request.POST,
            request.FILES,
            instance=project,
            user=request.user
        )
        if form.is_valid():
            project = form.save(commit=False)
            
            # Handle gold seed fields for faculty
            if request.user.groups.filter(name='Faculty').exists():
                project.is_gold = form.cleaned_data.get('is_gold', False)
                if project.is_gold:
                    project.token_reward = form.cleaned_data.get('token_reward')
                    project.gold_goal = form.cleaned_data.get('gold_goal')
                    project.deadline = form.cleaned_data.get('deadline')
                else:
                    # Clear gold seed fields if is_gold is False
                    project.token_reward = None
                    project.gold_goal = None
                    project.deadline = None
            
            project.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        # Initialize form with existing project data
        initial_data = {
            'is_gold': project.is_gold,
            'token_reward': project.token_reward,
            'gold_goal': project.gold_goal,
        }
        if project.deadline:
            initial_data['deadline'] = project.deadline.strftime('%Y-%m-%dT%H:%M')
            
        form = ProjectForm(
            instance=project,
            user=request.user,
            initial=initial_data
        )
    
    return render(request, 'projects/edit_project.html', {
        'form': form,
        'project': project,
        'title': 'Edit Project'
    })

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Delete associated files
    if project.featured_image:
        project.featured_image.delete()
    if project.pdf_file:
        project.pdf_file.delete()
    if project.additional_files:
        project.additional_files.delete()
        
    # Delete analytics data
    ProjectAnalytics.objects.filter(project=project).delete()
    
    # Delete notifications related to this project
    Notification.objects.filter(project=project).delete()
    
    # Delete the project
    project.delete()
    
    messages.success(request, 'Project deleted successfully')
    return redirect('projects:project_list')

@login_required
def clap_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        clap, created = Clap.objects.get_or_create(user=request.user, project=project)
        if created:
            project.clap_count += 1  # Use clap_count instead of clap_count
            project.save()
            return JsonResponse({'status': 'success', 'clap_count': project.clap_count})
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
    
    # Check permissions
    if comment.user != request.user and comment.project.author != request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('projects:project_detail', pk=comment.project.pk)
    
    try:
        project_pk = comment.project.pk
        comment.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        messages.success(request, 'Comment deleted successfully.')
        return redirect('projects:project_detail', pk=project_pk)
    
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        messages.error(request, f'Error deleting comment: {str(e)}')
        return redirect('projects:project_detail', pk=comment.project.pk)

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
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST)
        if form.is_valid():
            # Update notification settings
            user_profile.email_on_comment = form.cleaned_data['email_on_comment']
            user_profile.email_on_follow = form.cleaned_data['email_on_follow']
            user_profile.email_on_clap = form.cleaned_data['email_on_clap']
            user_profile.email_on_bookmark = form.cleaned_data['email_on_bookmark']
            user_profile.save()
            
            messages.success(request, 'Notification settings updated successfully!')
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



# Add to projects/views.py
def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)

def homepage(request):
    """Homepage view showing featured projects and recent activity"""
    # Get recent projects
    recent_projects = Project.objects.select_related('author').prefetch_related('comments').order_by('-created_at')[:6]
    
    # Get trending projects (most clap_count in last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    trending_projects = Project.objects.annotate(
        recent_claps=Count('clap_count', filter=Q(claps__created_at__gte=week_ago))
    ).order_by('-recent_claps', '-created_at')[:3]
    
    # Get top contributors
    top_contributors = get_monthly_contributions()[:5]
    
    # Get latest comments
    latest_comments = Comment.objects.select_related('user', 'project').order_by('-created_at')[:5]
    
    context = {
        'recent_projects': recent_projects,
        'trending_projects': trending_projects,
        'top_contributors': top_contributors,
        'latest_comments': latest_comments,
        'total_projects': Project.objects.count(),
        'total_users': User.objects.count(),
    }
    
    return render(request, 'projects/homepage.html', context)

def faculty_page(request):
    """View for the faculty page"""
    faculty_members = User.objects.filter(
        groups__name='Faculty'
    ).select_related('profile')
    
    context = {
        'faculty_members': faculty_members,
        'page_title': 'Faculty Members',
        'active_tab': 'faculty'
    }
    return render(request, 'projects/faculty_page.html', context)

def careers_page(request):
    return render(request, 'projects/careers.html', {
        'page_title': 'Careers',
        'active_tab': 'careers'
    })

@login_required
def clap_comment(request, pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        clap, created = CommentClap.objects.get_or_create(user=request.user, comment=comment)
        if created:
            comment.clap_count += 1
            comment.save()
            return JsonResponse({
                'status': 'success', 
                'claps': comment.clap_count,
                'commentId': comment.id
            })
        else:
            # Remove clap if already clapped
            clap.delete()
            comment.clap_count -= 1
            comment.save()
            return JsonResponse({
                'status': 'removed',
                'claps': comment.clap_count,
                'commentId': comment.id
            })
    return JsonResponse({'status': 'error'}, status=400)

def get_similar_projects(project, limit=3):
    """Returns similar projects based on tags"""
    if not project.tags:
        return Project.objects.exclude(id=project.id)[:limit]
    
    tags = [tag.strip() for tag in project.tags.split(',')]
    similar_projects = Project.objects.filter(
        tags__icontains=tags[0]
    ).exclude(id=project.id)
    
    for tag in tags[1:]:
        similar_projects = similar_projects | Project.objects.filter(
            tags__icontains=tag
        ).exclude(id=project.id)
    
    return similar_projects.distinct()[:limit]

def talents_page(request):
    # Get selected talent type from query params
    talent_type = request.GET.get('talent_type', '')
    
    # Base queryset
    talents = User.objects.annotate(
        project_count=Count('project'),
        follower_count=Count('followers'),
        following_count=Count('following')
    ).filter(
        ~Q(groups__name='Faculty'),
        is_active=True
    ).select_related('profile')
    
    # Apply talent type filter if selected
    if talent_type:
        talents = talents.filter(profile__talent_type=talent_type)
    
    talents = talents.order_by('-project_count')
    
    context = {
        'talents': talents,
        'title': 'Our Talents',
        'talent_types': TALENT_TYPES,
        'selected_talent': talent_type
    }
    return render(request, 'projects/talents.html', context)

@login_required
def submit_solution(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Check if project is a gold seed and still accepting submissions
    if not project.is_gold or not project.can_submit():
        messages.error(request, 'This project is not accepting submissions')
        return redirect('projects:project_detail', pk=pk)
    
    # Check if user already submitted
    if Solution.objects.filter(project=project, user=request.user).exists():
        messages.error(request, 'You have already submitted a solution')
        return redirect('projects:project_detail', pk=pk)
    
    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.project = project
            solution.user = request.user
            solution.save()
            messages.success(request, 'Solution submitted successfully!')
            return redirect('projects:project_detail', pk=pk)
    else:
        form = SolutionForm()
    
    return render(request, 'projects/submit_solution.html', {
        'form': form,
        'project': project
    })

@login_required
def review_solution(request, project_pk, solution_pk):
    solution = get_object_or_404(Solution, pk=solution_pk, project_id=project_pk)
    project = solution.project
    
    # Check if user is faculty and project author
    if not request.user.groups.filter(name='Faculty').exists() or request.user != project.author:
        messages.error(request, 'You do not have permission to review solutions')
        return redirect('projects:project_detail', pk=project_pk)
    
    if request.method == 'POST':
        is_approved = request.POST.get('is_approved') == 'true'
        feedback = request.POST.get('feedback', '')
        tokens = request.POST.get('tokens')
        
        solution.is_approved = is_approved
        solution.faculty_feedback = feedback
        if tokens and is_approved:
            solution.tokens_awarded = int(tokens)
        solution.save()
        
        messages.success(request, 'Solution review submitted successfully')
        return redirect('projects:project_detail', pk=project_pk)
    
    return render(request, 'projects/review_solution.html', {
        'solution': solution,
        'project': project
    })

@login_required
def join_team(request, team_slug):
    team = get_object_or_404(Team, slug=team_slug)
    
    # Check if user is already a member
    if TeamMembership.objects.filter(team=team, user=request.user).exists():
        messages.warning(request, 'You are already a member of this team.')
        return redirect('projects:team_detail', team_slug=team.slug)
    
    # Create membership
    TeamMembership.objects.create(
        team=team,
        user=request.user,
        role='member',
        is_approved=True  # Auto-approve for now, you can modify this for approval workflow
    )
    
    messages.success(request, f'You have successfully joined {team.name}!')
    return redirect('projects:team_detail', team_slug=team.slug)

@login_required
def leave_team(request, team_slug):
    team = get_object_or_404(Team, slug=team_slug)
    membership = get_object_or_404(TeamMembership, team=team, user=request.user)
    
    # Prevent founder from leaving
    if membership.role == 'founder':
        messages.error(request, 'Team founders cannot leave their team. Transfer ownership first or delete the team.')
        return redirect('projects:team_detail', team_slug=team.slug)
    
    # Delete membership
    membership.delete()
    
    messages.success(request, f'You have left {team.name}.')
    return redirect('projects:team_list')

@login_required
def promote_member(request, team_slug, user_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    team = get_object_or_404(Team, slug=team_slug)
    
    # Check if current user is founder
    if not TeamMembership.objects.filter(
        team=team,
        user=request.user,
        role='founder',
        is_approved=True
    ).exists():
        messages.error(request, 'Only team founders can promote members.')
        return redirect('projects:team_members', team_slug=team.slug)
    
    # Get target member
    membership = get_object_or_404(
        TeamMembership,
        team=team,
        user_id=user_id,
        is_approved=True
    )
    
    # Prevent promoting founder
    if membership.role == 'founder':
        messages.error(request, 'Cannot promote team founder.')
        return redirect('projects:team_members', team_slug=team.slug)
    
    # Promote to moderator
    membership.role = 'moderator'
    membership.save()
    
    messages.success(
        request, 
        f'{membership.user.get_full_name() or membership.user.username} has been promoted to moderator.'
    )
    return redirect('projects:team_members', team_slug=team.slug)

@login_required
def remove_member(request, team_slug, user_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    team = get_object_or_404(Team, slug=team_slug)
    
    # Check if current user is founder or moderator
    current_membership = get_object_or_404(
        TeamMembership,
        team=team,
        user=request.user,
        is_approved=True,
        role__in=['founder', 'moderator']
    )
    
    # Get target member
    membership = get_object_or_404(
        TeamMembership,
        team=team,
        user_id=user_id
    )
    
    # Prevent removing founder
    if membership.role == 'founder':
        messages.error(request, 'Cannot remove team founder.')
        return redirect('projects:team_members', team_slug=team.slug)
    
    # Prevent moderators from removing other moderators
    if current_membership.role == 'moderator' and membership.role == 'moderator':
        messages.error(request, 'Moderators cannot remove other moderators.')
        return redirect('projects:team_members', team_slug=team.slug)
    
    # Remove member
    membership.delete()
    
    messages.success(
        request, 
        f'{membership.user.get_full_name() or membership.user.username} has been removed from the team.'
    )
    return redirect('projects:team_members', team_slug=team.slug)

@login_required
def team_list(request):
    """
    Display a list of all teams with search and filter capabilities
    """
    teams = Team.objects.all().select_related('founder')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        teams = teams.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        ).distinct()
    
    # Filter by tags
    tag_filter = request.GET.get('tag', '')
    if tag_filter:
        teams = teams.filter(tags__icontains=tag_filter)
    
    # Get all unique tags for the filter dropdown
    all_tags = set()
    for team in Team.objects.values_list('tags', flat=True):
        if team:  # Check if tags exist
            all_tags.update(tag.strip() for tag in team.split(','))
    
    context = {
        'teams': teams,
        'search_query': search_query,
        'tag_filter': tag_filter,
        'all_tags': sorted(all_tags),
        'title': 'Teams'
    }
    
    return render(request, 'teams/team_list.html', context)

@login_required
def create_team(request):
    """
    Handle team creation
    """
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.founder = request.user
            team.save()
            
            # Create founder membership
            TeamMembership.objects.create(
                team=team,
                user=request.user,
                role='founder',
                is_approved=True
            )
            
            messages.success(request, f'Team "{team.name}" has been created successfully!')
            return redirect('projects:team_detail', team_slug=team.slug)
    else:
        form = TeamForm()
    
    return render(request, 'teams/create_team.html', {
        'form': form,
        'title': 'Create Team'
    })

@login_required
def team_detail(request, team_slug):
    """View for showing team details"""
    team = get_object_or_404(Team, slug=team_slug)
    
    # Get user's membership status
    user_membership = team.memberships.filter(user=request.user).first()
    
    # Get team members
    members = team.memberships.select_related('user').filter(is_approved=True)
    
    # Get team discussions
    discussions = team.discussions.select_related('author').order_by('-created_at')[:5]
    
    context = {
        'team': team,
        'user_membership': user_membership,
        'members': members,
        'discussions': discussions,
    }
    
    return render(request, 'teams/team_detail.html', context)
    


@login_required
def edit_team(request, team_slug):
    """
    Handle team editing
    """
    team = get_object_or_404(Team, slug=team_slug)
    
    # Check if user is founder or moderator
    membership = get_object_or_404(
        TeamMembership, 
        team=team, 
        user=request.user, 
        is_approved=True,
        role__in=['founder', 'moderator']
    )
    
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            team = form.save()
            messages.success(request, f'Team "{team.name}" has been updated successfully!')
            return redirect('projects:team_detail', team_slug=team.slug)
    else:
        form = TeamForm(instance=team)
    
    context = {
        'form': form,
        'team': team,
        'title': f'Edit Team: {team.name}',
        'can_delete': membership.role == 'founder'  # Only founders can delete teams
    }
    
    return render(request, 'teams/edit_team.html', context)

@login_required
def delete_team(request, team_slug):
    """
    Handle team deletion
    """
    team = get_object_or_404(Team, slug=team_slug)
    
    # Check if user is founder
    if not TeamMembership.objects.filter(
        team=team,
        user=request.user,
        role='founder',
        is_approved=True
    ).exists():
        messages.error(request, 'Only team founders can delete teams.')
        return redirect('projects:team_detail', team_slug=team.slug)
    
    if request.method == 'POST':
        # Store team name for success message
        team_name = team.name
        
        # Delete team image if it exists
        if team.team_image:
            team.team_image.delete(save=False)
        
        # Delete the team and all related objects
        team.delete()
        
        messages.success(request, f'Team "{team_name}" has been deleted successfully.')
        return redirect('projects:team_list')
    
    return render(request, 'teams/delete_team.html', {
        'team': team,
        'title': f'Delete Team: {team.name}'
    })

@login_required
def team_members(request, team_slug):
    """
    Display and manage team members
    """
    team = get_object_or_404(Team, slug=team_slug)
    
    # Get user's membership if exists
    user_membership = TeamMembership.objects.filter(
        team=team,
        user=request.user,
        is_approved=True
    ).first()
    
    # Check if user is a member
    if not user_membership:
        messages.error(request, 'You must be a team member to view this page.')
        return redirect('projects:team_detail', team_slug=team.slug)
    
    # Get all team members with profiles
    members = TeamMembership.objects.filter(
        team=team,
        is_approved=True
    ).select_related(
        'user',
        'user__profile'
    ).order_by(
        # Order by role (founder first, then moderators, then members)
        Case(
            When(role='founder', then=0),
            When(role='moderator', then=1),
            default=2
        ),
        'user__username'
    )
    
    # Get pending join requests if user is founder or moderator
    pending_requests = []
    if user_membership.role in ['founder', 'moderator']:
        pending_requests = TeamMembership.objects.filter(
            team=team,
            is_approved=False
        ).select_related('user', 'user__profile')
    
    context = {
        'team': team,
        'user_membership': user_membership,
        'members': members,
        'pending_requests': pending_requests,
        'title': f'{team.name} - Members',
        'can_manage': user_membership.role in ['founder', 'moderator']
    }
    
    return render(request, 'teams/team_members.html', context)

def help_view(request):
    return render(request, 'help.html', {
        'active_tab': 'Help'
    })


    ############################




# Class-based views for new features
class StartupListView(generic.ListView):
    model = Startup
    template_name = 'projects/startups/startup_list.html'
    context_object_name = 'startups'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class StartupCreateView(LoginRequiredMixin, generic.CreateView):
    model = Startup
    form_class = StartupForm
    template_name = 'projects/startups/startup_form.html'
    
    def form_valid(self, form):
        form.instance.founder = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:startup_list')

class ToolListView(generic.ListView):
    model = Tool
    template_name = 'projects/tools/tool_list.html'
    context_object_name = 'tools'

class ToolCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tool
    form_class = ToolForm
    template_name = 'projects/tools/tool_form.html'
    
    def get_success_url(self):
        return reverse('projects:tool_list')

class DatasetListView(generic.ListView):
    model = Dataset
    template_name = 'projects/datasets/dataset_list.html'
    context_object_name = 'datasets'

class DatasetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name = 'projects/datasets/dataset_form.html'
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.size = instance.file.size
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:dataset_list')

class SponsorshipListView(generic.ListView):
    model = Sponsorship
    template_name = 'projects/sponsorships/sponsorship_list.html'
    context_object_name = 'sponsorships'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group sponsorships by level
        sponsorships = {}
        for level, _ in Sponsorship.LEVELS:
            sponsorships[level] = self.get_queryset().filter(level=level)
        context['sponsorships'] = sponsorships
        return context

class VirtualMemberListView(generic.ListView):
    model = VirtualMember
    template_name = 'projects/virtual_members/virtual_member_list.html'
    context_object_name = 'virtual_members'

class ApplicationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'projects/application_form.html'
    success_url = reverse_lazy('projects:homepage')

    def get_initial(self):
        initial = super().get_initial()
        initial['type'] = self.request.GET.get('type', 'team')
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        application_type = self.request.GET.get('type')
        
        # Remove sponsor-specific fields for team applications
        if application_type != 'sponsor':
            del form.fields['organization']
            del form.fields['level']
        
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your application has been submitted successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_sponsor'] = self.request.GET.get('type') == 'sponsor'
        return context

@login_required
def download_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    zip_path = project.generate_zip()
    
    with open(zip_path, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{project.slug}_project.zip"'
    
    # Clean up the temporary zip file
    os.remove(zip_path)
    return response

@login_required
def download_dataset(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    
    # Increment download counter
    dataset.downloads += 1
    dataset.save()
    
    response = HttpResponse(dataset.file, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{dataset.name}.zip"'
    return response

class ApplicationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Application
    fields = ['type', 'cover_letter', 'resume', 'additional_info']
    template_name = 'projects/application_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def faq(request):
    return render(request, 'projects/faq.html')

@login_required
def team_discussions(request, team_slug):
    """View for showing team discussions"""
    team = get_object_or_404(Team, slug=team_slug)
    
    # Get user's membership status
    user_membership = TeamMembership.objects.filter(
        team=team,
        user=request.user,
        is_approved=True
    ).first()
    
    if not user_membership:
        messages.error(request, "You must be an approved team member to view discussions.")
        return redirect('projects:team_detail', team_slug=team.slug)
    
    # Get discussions
    discussions = team.discussions.select_related('author').order_by('-pinned', '-created_at')
    
    # Handle new discussion creation
    if request.method == 'POST':
        form = TeamDiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.team = team
            discussion.author = request.user
            discussion.save()
            
            # Update analytics if they exist
            if hasattr(team, 'analytics'):
                team.analytics.update_stats()
            
            messages.success(request, 'Discussion created successfully!')
            return redirect('projects:discussion_detail', 
                          team_slug=team.slug, 
                          discussion_id=discussion.id)
    else:
        form = TeamDiscussionForm()
    
    context = {
        'team': team,
        'discussions': discussions,
        'form': form,
        'user_membership': user_membership
    }
    
    return render(request, 'teams/team_discussions.html', context)

@login_required
def discussion_detail(request, team_slug, discussion_id):
    """View for showing discussion details and handling comments"""
    team = get_object_or_404(Team, slug=team_slug)
    discussion = get_object_or_404(TeamDiscussion, id=discussion_id, team=team)
    
    # Get user's membership status without notification preferences
    user_membership = TeamMembership.objects.filter(
        team=team,
        user=request.user,
        is_approved=True
    ).first()
    
    if not user_membership:
        messages.error(request, "You must be an approved team member to view discussions.")
        return redirect('projects:team_detail', team_slug=team.slug)
    
    # Handle new comment submission
    if request.method == 'POST':
        form = TeamCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            
            # Update analytics if they exist
            if hasattr(team, 'analytics'):
                team.analytics.update_stats()
            
            messages.success(request, 'Comment added successfully!')
            return redirect('projects:discussion_detail', 
                          team_slug=team.slug, 
                          discussion_id=discussion.id)
    else:
        form = TeamCommentForm()
    
    # Get comments
    comments = discussion.comments.select_related('author').order_by('created_at')
    
    context = {
        'team': team,
        'discussion': discussion,
        'comments': comments,
        'form': form,
        'user_membership': user_membership
    }
    
    return render(request, 'teams/discussion_detail.html', context)

@login_required
def pin_discussion(request, team_slug, discussion_id):
    """Toggle pin status of a discussion"""
    team = get_object_or_404(Team, slug=team_slug)
    discussion = get_object_or_404(TeamDiscussion, id=discussion_id, team=team)
    
    # Check if user is team moderator or founder
    membership = get_object_or_404(
        TeamMembership,
        team=team,
        user=request.user,
        role__in=['founder', 'moderator'],
        is_approved=True
    )
    
    discussion.pinned = not discussion.pinned
    discussion.save()
    
    return JsonResponse({
        'status': 'success',
        'pinned': discussion.pinned
    })

@login_required
def team_analytics(request, team_slug):
    """View for showing team analytics"""
    team = get_object_or_404(Team, slug=team_slug)
    
    # Check if user is team moderator or founder
    membership = get_object_or_404(
        TeamMembership,
        team=team,
        user=request.user,
        role__in=['founder', 'moderator'],
        is_approved=True
    )
    
    # Get time ranges
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    seven_days_ago = now - timedelta(days=7)
    
    # Calculate analytics
    analytics = {
        'total_discussions': team.discussions.count(),
        'total_comments': TeamComment.objects.filter(discussion__team=team).count(),
        'discussions_this_month': team.discussions.filter(created_at__gte=thirty_days_ago).count(),
        'comments_this_month': TeamComment.objects.filter(
            discussion__team=team,
            created_at__gte=thirty_days_ago
        ).count(),
        'discussions_this_week': team.discussions.filter(created_at__gte=seven_days_ago).count(),
        'comments_this_week': TeamComment.objects.filter(
            discussion__team=team,
            created_at__gte=seven_days_ago
        ).count(),
        'active_members': TeamMembership.objects.filter(
            team=team,
            user__last_login__gte=thirty_days_ago
        ).count()
    }
    
    # Get member activity
    member_activity = TeamMembership.objects.filter(
        team=team,
        is_approved=True
    ).annotate(
        discussions_count=Count('user__teamdiscussion', filter=Q(user__teamdiscussion__team=team)),
        comments_count=Count('user__teamcomment', filter=Q(user__teamcomment__discussion__team=team)),
        last_activity=models.Max(
            Case(
                When(user__teamdiscussion__team=team, then='user__teamdiscussion__created_at'),
                When(user__teamcomment__discussion__team=team, then='user__teamcomment__created_at'),
                default=models.F('created_at')
            )
        )
    ).order_by('-last_activity')
    
    # Calculate activity score
    activity_score = (
        (analytics['discussions_this_month'] * 5) +  # Weight discussions more
        analytics['comments_this_month']
    ) / max(analytics['active_members'], 1)  # Avoid division by zero
    
    return render(request, 'teams/team_analytics.html', {
        'team': team,
        'analytics': analytics,
        'member_activity': member_activity,
        'activity_score': round(activity_score, 1)
    })

@login_required
def delete_discussion(request, team_slug, discussion_id):
    """Delete a team discussion"""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
        
    team = get_object_or_404(Team, slug=team_slug)
    discussion = get_object_or_404(TeamDiscussion, id=discussion_id, team=team)
    
    # Check if user is author, moderator, or founder
    user_membership = get_object_or_404(
        TeamMembership,
        team=team,
        user=request.user,
        is_approved=True
    )
    
    if not (discussion.author == request.user or 
            user_membership.role in ['moderator', 'founder']):
        raise PermissionDenied("You don't have permission to delete this discussion.")
    
    try:
        # Delete the discussion
        discussion.delete()
        
        # Update analytics if they exist
        if hasattr(team, 'analytics'):
            team.analytics.update_stats()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Discussion deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# Contents from: .\views\analytics.py
# projects/views/analytics.py

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.shortcuts import render
from ..models.analytics import PageVisit, EventTracker

@staff_member_required
def analytics_dashboard(request):
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timezone.timedelta(days=days)

    # Get basic stats
    total_visits = PageVisit.objects.filter(timestamp__gte=start_date).count()
    unique_visitors = PageVisit.objects.filter(timestamp__gte=start_date).values('user', 'ip_address').distinct().count()
    
    # Get daily visits
    daily_visits = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        date=TruncDate('timestamp')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Get popular pages
    popular_pages = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).values('path').annotate(
        visits=Count('id')
    ).order_by('-visits')[:10]

    # Get device breakdown
    devices = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).values('device_type').annotate(
        count=Count('id')
    )

    # Get browser breakdown
    browsers = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).values('browser').annotate(
        count=Count('id')
    )

    context = {
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'daily_visits': daily_visits,
        'popular_pages': popular_pages,
        'devices': devices,
        'browsers': browsers,
        'days': days,
    }

    return render(request, 'analytics/dashboard.html', context)