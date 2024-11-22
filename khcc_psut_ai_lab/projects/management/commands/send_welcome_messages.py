# projects/management/commands/send_welcome_messages.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import (
    Team, 
    TeamMembership, 
    KHCCBrain,
    TeamDiscussion,
    User
)

class Command(BaseCommand):
    help = 'Sends welcome messages to teams KHCC Brain has joined'

    def handle(self, *args, **options):
        self.stdout.write("\n=== Starting Welcome Messages Process ===")
        
        try:
            # Get KHCC Brain user
            KHCC_brain_user = User.objects.get(username='KHCC_brain')
            
            # Get teams where KHCC Brain is a member
            memberships = TeamMembership.objects.filter(user=KHCC_brain_user)
            
            for membership in memberships:
                team = membership.team
                
                # Check if welcome message already exists
                existing_welcome = TeamDiscussion.objects.filter(
                    team=team,
                    author=KHCC_brain_user,
                    title="KHCC Brain Introduction"
                ).exists()
                
                if not existing_welcome:
                    # Create welcome message
                    welcome_message = f"""
Hello {team.name} team! 👋

I'm KHCC Brain, your AI research assistant, and I'm excited to join this team. I'm here to help with:

• Analyzing discussions and providing insights
• Suggesting potential research directions
• Offering relevant healthcare AI perspectives
• Identifying collaboration opportunities

Feel free to mention me in any discussions where you'd like my input. I'll be actively monitoring our team's conversations and contributing where I can help most.

Looking forward to collaborating with everyone!

Best regards,
KHCC Brain 🤖
                    """
                    
                    discussion = TeamDiscussion.objects.create(
                        team=team,
                        author=KHCC_brain_user,
                        title="KHCC Brain Introduction",
                        content=welcome_message
                    )
                    
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Posted welcome message to team: {team.name}"
                    ))
                else:
                    self.stdout.write(f"Welcome message already exists for team: {team.name}")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
            
        self.stdout.write("\n=== Welcome Messages Process Complete ===")