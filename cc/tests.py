from datetime import date
from sys import stderr as prnt

from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase, RequestFactory

from cc.models import MonthlyPosts
from cc.views import verifyUser


# ------ LOGIN ------ #

class LoginTest(TestCase):
    
    #overriding method in 'TestCase'
    def setUp(self):
        User.objects.create_user(username='carrieUser', password='carriespassword')
        User.objects.create_user(username='parent', password='parentpassword')

    #Test the Login and redirect systems for various users
    def test_carrie_login_redirect(self):
        
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200, msg_prefix="", fetch_redirect_response=False)
        # '/' is synonymous with the login screen, but I am thinking that I should make this url the home screen from now on, and start implementing reverse()
    
    def test_carrie_login(self):
        response = self.client.post(reverse('home'))
        self.assertTrue(response.status_code, 302)
        
        self.factory = RequestFactory()
        request = self.factory.post('/login/', {'password_field' : 'carriespassword'})
        request.session = self.client.session
        verifyUser(request)
        
        response = self.client.get('/home/')
        
        
# ------ HOMEPAGE ------ #

#view
class HomepageViewTest(TestCase):
    
    def test_navbar(self):
        self.assertTrue(False)
    
    def test_calendar_appears(self):
        self.assertTrue(False)

#model and form
class MonthlyPostsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        #make 10 uninteresting posts
        for i in range(1,11):
            nTitle = "Title: {0}".format(i)
            nText = "this is the body {0}".format(i)
            nPublish_date = date(1994, i, 9)
            MonthlyPosts.objects.create(title=nTitle, text=nText, publish_date = nPublish_date)
    
    #Unit Tests
        
    def test_retrieve_a_post(self):
        post = MonthlyPosts.objects.get(title="Title: 1")
        self.assertEquals(post.text, "this is the body 1")
        
    def test_edit_a_post(self):
        post = MonthlyPosts.objects.get(title="Title: 3")
        post.text = "this is the NEW body.  You like?"
        post.save()
        updatedPost = MonthlyPosts.objects.get(title="Title: 3")
        self.assertEquals(updatedPost.text, "this is the NEW body.  You like?")
        
    def test_delete_a_post(self):
        MonthlyPosts.objects.get(title="Title: 5").delete()
        self.assertEquals(MonthlyPosts.objects.count(), 9)
        
    #Integrated Tests

    def test_create_and_retrieve_a_post(self):
        self.assertTrue(False)

        
    def test_create_and_display_a_post(self):
        self.assertTrue(False)
        
    
