from django.test import TestCase
from .models import BlogPosts
from datetime import date


#testing models

class BlogPostsModelTest(TestCase):
    def test_create_post(self):
        post = self.createBlogPost()
        
        self.assertEquals(post.__str__(), 'Title: 1')
    
    def createBlogPost(self):
        return BlogPosts(title="Title: 1", text="this is the body", publish_date = date(1994, 5, 9))