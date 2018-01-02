from django.test import TestCase
from .models import BlogPosts, Links

class BlogPostsModelTest(TestCase):
    def test_create_post(self):
        #create a blogpost
        
        self.assertEquals(self.getblogPost(), 'First blog post')
    
    def setBlogPost(self):
        return 0
    
    def getBlogPost(self):
        return 0