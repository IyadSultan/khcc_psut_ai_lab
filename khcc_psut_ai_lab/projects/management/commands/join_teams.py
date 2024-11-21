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
            kcc_brain_user = KHCCBrain.get_user()
            self.stdout.write(self.style.SUCCESS(
                f"✓ KHCC Brain user exists: {kcc_brain_user.username}"
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
        if kcc_brain_user:
            memberships = TeamMembership.objects.filter(user=kcc_brain_user)
            if memberships.exists():
                self.stdout.write("KHCC Brain is member of:")
                for membership in memberships:
                    self.stdout.write(f"- {membership.team.name} (Role: {membership.role})")
            else:
                self.stdout.write(self.style.WARNING("KHCC Brain is not a member of any teams"))

        # 4. Try to join teams
        self.stdout.write("\n=== Attempting to Join Teams ===")
        if kcc_brain_user:
            new_teams = Team.objects.exclude(memberships__user=kcc_brain_user)
            if new_teams.exists():
                for team in new_teams:
                    try:
                        membership, created = TeamMembership.objects.get_or_create(
                            team=team,
                            user=kcc_brain_user,
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
            kcc_brain_user = KHCCBrain.get_user()
            self.stdout.write(f"Found KHCC Brain user: {kcc_brain_user.username}")

            # Get all teams
            all_teams = Team.objects.all()
            self.stdout.write(f"Found {all_teams.count()} total teams")

            # Get teams KHCC Brain hasn't joined
            new_teams = Team.objects.exclude(
                memberships__user=kcc_brain_user
            )
            self.stdout.write(f"Found {new_teams.count()} teams to join")

            # Join each team
            for team in new_teams:
                try:
                    membership = TeamMembership.objects.create(
                        team=team,
                        user=kcc_brain_user,
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