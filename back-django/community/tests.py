from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from books.models import Book
from .models import Thread, Comment

User = get_user_model()

class CommunityIntegrationTest(APITestCase):
    def setUp(self):
        # 1. Prepare Users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # 2. Prepare Book
        self.book = Book.objects.create(
            isbn13='9780000000001',
            title='Test Book',
            author='Test Author',
            publisher='Test Publisher',
            cover='http://example.com/cover.jpg',
            descriptions='Test Descriptions'
        )

        # 3. Get Tokens (Simulate Login)
        response1 = self.client.post('/accounts/api/token/', {'username': 'user1', 'password': 'password123'})
        self.token1 = response1.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        
        # User2 Token
        response2 = self.client.post('/accounts/api/token/', {'username': 'user2', 'password': 'password123'})
        self.token2 = response2.data['access']

    def test_full_community_flow(self):
        """
        Scenario:
        1. User1 posts a Thread (Review).
        2. User2 reads the Thread.
        3. User2 likes the Thread.
        4. User2 comments on the Thread.
        5. User1 deletes the Thread.
        """

        # 1. User1 Create Thread
        url_create = '/api/v1/community/threads/'
        data = {
            'book_isbn13': self.book.isbn13,
            'title': 'My Review',
            'content': 'Great book!',
            'rating': 5
        }
        response = self.client.post(url_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        thread_id = response.data['id']
        
        # 2. User2 Read Thread
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token2) # Switch to User2
        url_detail = f'/api/v1/community/threads/{thread_id}/'
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'My Review')

        # 3. User2 Like Thread
        url_like = f'/api/v1/community/threads/{thread_id}/likes/'
        response = self.client.post(url_like)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['liked'])
        self.assertEqual(response.data['count'], 1)

        # 4. User2 Comment
        url_comment = f'/api/v1/community/threads/{thread_id}/comments/'
        data_comment = {'content': 'Nice review!'}
        response = self.client.post(url_comment, data_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment_id = response.data['id']

        # Verify Comment appears in Thread Detail
        response = self.client.get(url_detail)
        self.assertEqual(len(response.data['comments']), 1)
        self.assertEqual(response.data['comments'][0]['content'], 'Nice review!')

        # 5. User1 Delete Thread
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1) # Switch back to User1 (Owner)
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check deletion
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_flow(self):
        """
        Scenario:
        1. User1 follows User2.
        2. Check profile stats.
        3. User1 unfollows User2.
        """
        # User1 follows User2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token1)
        url_follow = f'/accounts/follow/{self.user2.id}/'
        
        # Follow
        response = self.client.post(url_follow)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['followed'])

        # Check User2 Profile (should have 1 follower)
        # Note: In our current implementation, we fetch profile by username
        response = self.client.get(f'/accounts/profile/{self.user2.username}/')
        # Serializer returns list of followers IDs
        followers = response.data['followers']
        # followers is list of objects now based on serializer change {id, username}
        self.assertTrue(any(f['username'] == 'user1' for f in followers))

        # Unfollow
        response = self.client.post(url_follow)
        self.assertFalse(response.data['followed'])
