from datetime import date
from sys import stderr as prnt
from time import sleep 

from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase, RequestFactory

from cc.models import MonthlyPosts
from cc.views import verifyUser


# ------ LOGIN ------ #

class LoginTest(TestCase):
    
    #Overriding method in 'TestCase'
    def setUp(self):
        self.factory = RequestFactory()
        
        User.objects.create_user(username='carrieUser', email="carrie@notmail.com", password='carriespassword')
        User.objects.create_user(username='parent', email="carrie@notmail.com", password='parentpassword')
        

    #Test the Login's redirect for users that are not logged in (tests for logged-in users occur later) 
    def test_login_redirect(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200, msg_prefix="", fetch_redirect_response=False)
        
    #Test the responses from verifyUser(), authentication tests occur later
    def test_verifyUser(self):
        request = self.factory.post('/login/', {'password_field' : 'carriespassword'})
        request.session = self.client.session
        response = verifyUser(request)
        
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200, msg_prefix="", fetch_redirect_response=False)
        self.assertEqual(response.url, reverse('home'))
    
    def test_carrie_login(self):
        self.attempt_login_with_password('carriespassword')
        
    def attempt_login_with_password(self, password):
        # redirects before login
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        
        # no 'user' until after login
        self.assertIsNone(response.context)
        response = self.client.post(reverse('login'), {'password_field' : password}, follow=True)
        self.assertIsNotNone(response.context)
        self.assertTrue(response.context['user'].is_authenticated())
        
        # no longer redirects
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
    def test_carrie_permissions(self):
        self.fail("not yet implemented")
        
    def test_parent_login(self):
        self.attempt_login_with_password('parentpassword')
    
    def test_parent_permissions(self):
        self.fail("not yet implemented")
        
    def test_incorrect_login(self):
        # redirects before login
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        
        # no 'user' until after login
        self.assertIsNone(response.context)
        response = self.client.post(reverse('login'), {'password_field' : 'incorrectpassword'}, follow=True)
        self.assertIsNotNone(response.context)
        # user is not authenticated
        self.assertFalse(response.context['user'].is_authenticated())
        
        # still redirects, and 
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        
    def test_cookie_expiration(self):
        self.fail("not yet implemented")
        
        # this is new 
        
        # I can't figure out how to render the homepage again without it resetting the resuest.session's expiration time....it works when I manually enter it 
        # though (change the 'homepage' view function to have 'expTime' = .5 and then sleep(1) between client.get()'s.    
        
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
        
    
