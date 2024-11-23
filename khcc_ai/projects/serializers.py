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