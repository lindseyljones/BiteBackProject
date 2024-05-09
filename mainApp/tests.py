from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import connection
from mainApp.models import Post, PostForm
# Create your tests here.
class PostModelTest(TestCase):
    def tearDown(self):
        Post.objects.all().delete()
    
        query = 'ALTER SEQUENCE "mainApp_post_id_seq" RESTART WITH 1'
    
        cursor = connection.cursor()
    
        cursor.execute(query)

    def setUp(self):
        Post.objects.create(id=1, title='Testing123', description='Description123')
        Post.objects.create(id=2, title='', description='Description123', file=None)
    def test_title(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'Testing123')
    def test_description(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.description, 'Description123')
#    def test_title_error(self):
#        post = Post.objects.get(id=2)
#        post.full_clean()
#       self.assertRaises(ValidationError)