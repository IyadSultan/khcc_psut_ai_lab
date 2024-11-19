from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Team, TeamMembership

class TeamAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.team = Team.objects.create(
            name='Test Team',
            description='Test Description',
            founder=self.user
        )
        TeamMembership.objects.create(
            team=self.team,
            user=self.user,
            role='founder',
            is_approved=True
        )

    def test_team_list_api(self):
        response = self.client.get(reverse('api_team_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_team_detail_api(self):
        response = self.client.get(reverse('api_team_detail', args=[self.team.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Team')

    def test_team_analytics_api(self):
        response = self.client.get(reverse('api_team_analytics', args=[self.team.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_discussions', response.data)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(reverse('api_team_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)