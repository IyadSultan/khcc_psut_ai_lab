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
            try:
                project = form.save(commit=False)
                project.author = request.user
                project.save()
                
                # Create project directory
                project_dir = f'uploads/user_{request.user.id}/project_{project.id}'
                os.makedirs(os.path.join(settings.MEDIA_ROOT, project_dir), exist_ok=True)
                
                messages.success(request, 'Project submitted successfully!')
                return redirect('projects:project_detail', pk=project.pk)
            except Exception as e:
                messages.error(request, f'Error saving project: {str(e)}')
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
            
            # Handle replies
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            
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
            return redirect('projects:project_detail', pk=pk)
        else:
            messages.error(request, 'Error posting comment. Please check your input.')
    else:
        form = CommentForm()
    
    context = {
        'project': project,
        'comments': comments,
        'comment_form': form,
        'featured_image_url': project.get_featured_image_url(),
        'pdf_url': project.get_pdf_url(),
        'rating_form': RatingForm(),
    }
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
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

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
    
    # Get trending projects (most claps in last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    trending_projects = Project.objects.annotate(
        recent_claps=Count('claps', filter=Q(claps__created_at__gte=week_ago))
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