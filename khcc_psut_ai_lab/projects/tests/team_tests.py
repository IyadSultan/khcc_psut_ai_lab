from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Team, TeamMembership, TeamDiscussion, TeamComment
from datetime import timedelta
from django.utils import timezone

class TeamTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Description',
            founder=self.user,
            max_members=10
        )
        TeamMembership.objects.create(
            team=self.team,
            user=self.user,
            role='founder',
            is_approved=True
        )

    def test_team_creation(self):
        response = self.client.post(reverse('create_team'), {
            'name': 'New Team',
            'description': 'New Description',
            'max_members': 15
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name='New Team').exists())

    def test_team_join(self):
        new_user = User.objects.create_user('newuser', 'new@test.com', 'newpass')
        self.client.login(username='newuser', password='newpass')
        
        response = self.client.post(reverse('join_team', args=[self.team.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamMembership.objects.filter(
            team=self.team,
            user=new_user,
            is_approved=False
        ).exists())

    def test_discussion_creation(self):
        response = self.client.post(
            reverse('create_discussion', args=[self.team.slug]),
            {
                'title': 'Test Discussion',
                'content': 'Test Content'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamDiscussion.objects.filter(
            team=self.team,
            title='Test Discussion'
        ).exists())

    def test_analytics_updates(self):
        discussion = TeamDiscussion.objects.create(
            team=self.team,
            author=self.user,
            title='Test Discussion',
            content='Test Content'
        )
        
        analytics = self.team.analytics
        self.assertEqual(analytics.total_discussions, 1)
        self.assertEqual(analytics.discussions_this_week, 1)

        TeamComment.objects.create(
            discussion=discussion,
            author=self.user,
            content='Test Comment'
        )
        
        analytics.refresh_from_db()
        self.assertEqual(analytics.total_comments, 1)
        self.assertEqual(analytics.comments_this_week, 1)

    def test_notification_preferences(self):
        membership = TeamMembership.objects.get(team=self.team, user=self.user)
        membership.notification_preferences = {
            'email_notifications': False,
            'in_app_notifications': True
        }
        membership.save()
        
        membership.refresh_from_db()
        self.assertFalse(membership.notification_preferences['email_notifications'])
        self.assertTrue(membership.notification_preferences['in_app_notifications'])

    def test_member_permissions(self):
        regular_user = User.objects.create_user('regular', 'regular@test.com', 'pass')
        membership = TeamMembership.objects.create(
            team=self.team,
            user=regular_user,
            role='member',
            is_approved=True
        )
        
        self.client.login(username='regular', password='pass')
        
        # Try to access team settings (should be forbidden)
        response = self.client.get(reverse('team_settings', args=[self.team.slug]))
        self.assertEqual(response.status_code, 403)

        # Can create discussions
        response = self.client.post(
            reverse('create_discussion', args=[self.team.slug]),
            {'title': 'Member Discussion', 'content': 'Content'}
        )
        self.assertEqual(response.status_code, 302)