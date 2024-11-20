from datetime import datetime, timedelta
from io import StringIO
import csv
import json
import os
import pytz

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.db.models import Count, Q, Avg, Sum, Case, When
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from khcc_psut_ai_lab.constants import TALENT_TYPES, TALENT_DICT

from .filters.project_filters import ProjectFilter
from .forms import (
    ProjectForm, CommentForm, ProjectSearchForm, UserProfileForm,
    RatingForm, BookmarkForm, AdvancedSearchForm, ProfileForm, NotificationSettingsForm, ExtendedUserCreationForm,
    SolutionForm, TeamForm, TeamDiscussionForm, TeamCommentForm, TeamNotificationSettingsForm
)
from .models import (
    Project, Comment, Clap, UserProfile, Rating,
    Bookmark, ProjectAnalytics, Notification, Follow,
    CommentClap, Solution, Team, TeamMembership, TeamDiscussion, TeamComment, TeamAnalytics
)
from .serializers import ProjectSerializer, ProjectAnalyticsSerializer, ProjectAnalyticsSummarySerializer
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
    
    # Get per_page parameter from request, default to 12
    per_page = request.GET.get('per_page', 12)
    try:
        per_page = int(per_page)
        # Limit per_page to valid options
        if per_page not in [12, 24, 48]:
            per_page = 12
    except ValueError:
        per_page = 12
    
    # Pagination with dynamic per_page
    paginator = Paginator(projects, per_page)
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
        'per_page': per_page,
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
        'title': 'Submit Project'
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
    """
    Display team details, members, and activities
    """
    team = get_object_or_404(Team, slug=team_slug)
    
    # Get user's membership if exists
    user_membership = TeamMembership.objects.filter(
        team=team,
        user=request.user
    ).first()
    
    # Get team members with profiles
    members = TeamMembership.objects.filter(
        team=team,
        is_approved=True
    ).select_related('user', 'user__profile').order_by('-role', 'user__username')
    
    # Get recent activities (if you have an Activity model)
    # activities = team.activities.all().select_related('user')[:5]
    
    context = {
        'team': team,
        'user_membership': user_membership,
        'members': members,
        # 'activities': activities,
        'title': team.name,
        'tags': [tag.strip() for tag in team.tags.split(',')] if team.tags else []
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