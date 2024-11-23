def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        
        # If you need to redirect to a team-specific page, get the team from related objects
        # For example, if notification has a related_object that has a team:
        if hasattr(notification, 'related_object') and hasattr(notification.related_object, 'team'):
            team = notification.related_object.team
            return redirect('team_dashboard', team_id=team.id)
        
        # Default redirect if no team is found
        return redirect('notifications_list')
        
    except Notification.DoesNotExist:
        messages.error(request, 'Notification not found.')
        return redirect('notifications_list') 