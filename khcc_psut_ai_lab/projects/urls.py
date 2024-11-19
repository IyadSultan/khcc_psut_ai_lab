# projects/urls.py

from django.urls import path
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
    
    # User Profiles - Note the reordered URLs
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Moved before username pattern
    path('profile/settings/', views.profile_settings, name='profile_settings'),  # Added settings
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
    
    # API Endpoints
    path('api/projects/', views.ProjectListAPI.as_view(), name='api_project_list'),
    path('api/projects/<int:pk>/', views.ProjectDetailAPI.as_view(), name='api_project_detail'),
    path('api/projects/<int:pk>/analytics/', views.ProjectAnalyticsAPI.as_view(), name='api_project_analytics'),
    path('faculty/', views.faculty_page, name='faculty_page'),
    path('careers/', views.careers_page, name='careers'),
    # urls.py
     path('comment/<int:pk>/clap/', views.clap_comment, name='clap_comment'),
     path('talents/', views.talents_page, name='talents'),
     path('project/<int:pk>/submit-solution/', views.submit_solution, name='submit_solution'),
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
]