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
    site_header = 'KHCC_PSUT AI Lab Administration'
    site_title = 'KHCC_PSUT AI Lab Admin'
    index_title = 'Dashboard'
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Add custom statistics to the admin index
        app_list.append({
            'name': 'Statistics',
            'app_label': 'statistics',
            'models': [
                {
                    'name': 'Total Projects',
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