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