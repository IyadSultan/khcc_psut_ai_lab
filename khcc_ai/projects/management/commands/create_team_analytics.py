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