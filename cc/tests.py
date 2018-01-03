from django.test import TestCase
from cc.models import BlogPosts
from datetime import date

import sys



""" LOGIN """

class LoginTest(TestCase):
    
    def test_login_password(self):
        self.assertTrue(False)
    



""" HOMEPAGE """

#view
class HomepageViewTest(TestCase):
    
    def test_navbar_links(self):
        self.assertTrue(False)
        
    def test_calendar_appears(self):
        self.assertTrue(False)

#models
class BlogPostsModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        #make 10 uninteresting posts
        for i in range(1,11):
            nTitle = "Title: {0}".format(i)
            nText = "this is the body {0}".format(i)
            nPublish_date = date(1994, i, 9)
            BlogPosts.objects.create(title=nTitle, text=nText, publish_date = nPublish_date)
    
    #Unit Tests
    
    def test_retrieve_a_post(self):
        post = BlogPosts.objects.get(title="Title: 1")
        self.assertEquals(post.text, "this is the body 1")
        
    def test_edit_a_post(self):
        post = BlogPosts.objects.get(title="Title: 3")
        post.text = "this is the NEW body.  You like?"
        post.save()
        updatedPost = BlogPosts.objects.get(title="Title: 3")
        self.assertEquals(updatedPost.text, "this is the NEW body.  You like?")
        
    def test_delete_a_post(self):
        BlogPosts.objects.get(title="Title: 5").delete()
        self.assertEquals(BlogPosts.objects.count(), 9)
        
    #Integrated Tests

    def test_create_and_retrieve_a_post(self):
        self.assertTrue(False)

        
    def test_create_and_display_a_post(self):
        self.assertTrue(False)

