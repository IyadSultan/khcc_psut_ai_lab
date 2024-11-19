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