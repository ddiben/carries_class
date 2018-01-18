# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

""" 
This is deprecated.  I switched to having the tests in a separate folder.  I kept this just in case. 

"""

from datetime import date
from sys import stderr as prnt
import time

from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase, RequestFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from cc.models import MonthlyPosts, Links
from cc.views import verifyUser, homepage, links

from cc.tests.ccTestCases import ccTestCase

# ------ Integrated Test ------ #

class IntegratedTest(StaticLiveServerTestCase):
    # This sequence of tests simulate all functionality of the site. The general structure is 'carrieUser' does something and then 'parent' verifies it. 
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome('/usr/local/bin/chromedriver')
        cls.selenium.implicitly_wait(5)
        
    def setUp(self):
        User.objects.create_user(username='carrieUser', password='carriespassword')
        User.objects.create_user(username='parent', password='parentpassword')
        

    def test_login(self):
        self.login('carriespassword')
        self.assertEqual('{0}{1}'.format(self.live_server_url, reverse('home')), self.selenium.current_url)  
        
        self.login('parentpassword') 
        self.assertEqual('{0}{1}'.format(self.live_server_url, reverse('home')), self.selenium.current_url)  

    def login(self, password):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        password_input = self.selenium.find_element_by_class_name('login-input')
        password_input.send_keys(password)
        self.selenium.find_element_by_class_name('login-submit').click()
        
    # 'carrie' edits and saves a post, and a 'parent' verifies those changes. 
    def test_edit_post(self):
        
        # --- carrie: edit ('save' button) ---
        
        """ Some cleanup to do: functionalize this in general, and isolate assertion statements for clearer debugging """
        
        self.login('carriespassword')
        
        post_header = self.selenium.find_element_by_id('monthly-header-form')
        post_text = self.selenium.find_element_by_id('monthly-text-form')
        post_submit = self.selenium.find_element_by_name('save')
        
        self.scan_page_for(["No post", "like there"])
        
        post_header.clear()
        post_text.clear()
        
        post_header.send_keys('tomatoes')
        post_text.send_keys('pickles')
        
        post_submit.click()
        
        self.scan_page_for(["tomatoes", "pickles"])
        # this was turning up in the 'source_code' without appearing on the page, so I am running a quick double check
        textarea = self.selenium.find_element_by_id('monthly-text-form')
        self.assertEqual(textarea.text, "pickles")
        
        # --- parent ---
        
        self.login('parentpassword')
        self.scan_page_for(["tomatoes", "pickles"])
        
        # --- carrie --- 'new' button
        
        self.login('carriespassword')
        post_new = self.selenium.find_element_by_name("new")
        post_new.click()
        
        allPosts = MonthlyPosts.objects.all()
        self.assertEqual(len(allPosts), 2)
        # one for the previous, and one for the blank post that was created by 'new'. 
        
        self.scan_page_for(["blank title", "write something new"])
        
        post_header = self.selenium.find_element_by_id('monthly-header-form')
        post_text = self.selenium.find_element_by_id('monthly-text-form')
        post_submit = self.selenium.find_element_by_name('save')
        
        post_header.clear()
        post_text.clear()
        
        post_header.send_keys("tomatoes2")
        post_text.send_keys("pickles2")
        
        post_submit.click() # why is this overriding the previous post, which shouldn't be accessible
        
        self.scan_page_for(["tomatoes2", "pickles2"])
        
        post_new = self.selenium.find_element_by_name("new")
        post_new.click()
         
        self.scan_page_for(["blank title", "write something new"])
        
        post_header = self.selenium.find_element_by_id('monthly-header-form')
        post_text = self.selenium.find_element_by_id('monthly-text-form')
        post_submit = self.selenium.find_element_by_name('save')
        
        post_header.clear()
        post_text.clear()
        
        post_header.send_keys("tomatoes3")
        post_text.send_keys("pickles3")
        
        post_submit.click()
        
        allPosts = MonthlyPosts.objects.all()
        
        for post in allPosts:
            prnt.write(repr(post))
        
        self.assertEqual(len(allPosts), 3)
        
        # --- parent ---
        
        self.login('parentpassword')
        
        self.scan_page_for(["tomatoes3", "pickles3"])
    
    def scan_page_for(self, listOfStrings):
        page = self.selenium.page_source
        for search_string in listOfStrings:
            assert search_string in page
            
    def create_and_edit_links(self):
        
        self.login('carriespassword')
        
        self.selenium.find_element_by_name('links_lnk').click()
        
        self.selenium.find_element_by_name('new').click()
        
        self.selenium.find_element_by_class('link-form-title')
        self.selenium.find_element_by_class('link-form-description')
        
        # parent verifies that its there
        
        # create two more links, and edit the old link
        
        # parent verifies that all of them are there and correctly rendered
        
        # delete a link and make sure that it is deleted from the database (SHOULD THEY ALL BE PERSISTED??)
        
        self.fail("not yet implemented")
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        
    
# ------ LOGIN ------ #

class LoginTest(ccTestCase):
    
    #Overriding method in 'TestCast'
    def setUp(self):
        super().setUp()
        
        self.factory = RequestFactory()
        
    #Test the Login's redirect for users that are not logged in (tests for logged-in users occur later) 
    def test_login_redirect(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200, msg_prefix="", fetch_redirect_response=False)
        
    #Test the responses from verifyUser(), authentication tests occur later
    def test_verifyUser(self):
        request = self.factory.post(reverse('login'), {'password_field' : 'carriespassword'})
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
        
    def test_parent_login(self):
        self.attempt_login_with_password('parentpassword')
        
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
    
        request = self.factory.get(reverse('home'))
        request.session = self.client.session
        request.user = User.objects.get(username='carrieUser')
        
        homepage(request, expTime=.5)
        
        self.assertEqual(request.session['_session_expiry'], .5) 
        
        # I think I need another view other than the home view to try and access, so that the 'request._session_expiry' doesn't get reset.
        
        # I can't figure out how to render the homepage again without it resetting the resuest.session's expiration time....it works when I manually enter it 
        # though (change the 'homepage' view function to have 'expTime' = .5 and then sleep(1) between client.get('home')'s.    
        

# ------ HOMEPAGE ------ #

# view
class HomepageViewTest(ccTestCase):
        
    def test_links_of_navbar(self):
        self.assertTrue(False)
        
# model
class MonthlyPostsTest(ccTestCase):
    
    @classmethod
    def setUpTestData(cls):
        #make 10 uninteresting posts
        for i in range(1,11):
            nTitle = "Title: {0}".format(i)
            nText = "this is the body {0}".format(i)
            nPublish_date = date(1994, i, 9)
            MonthlyPosts.objects.create(title=nTitle, text=nText, publish_date = nPublish_date)
            
        
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
        
    def test_set_post_to_display(self):
         
        qs = MonthlyPosts.objects.get(title="Title: 7")
        qs.set_post_to_display()
        qs.save()
        mp = MonthlyPosts.objects.get(to_display=True)
        
        self.assertEqual(mp, MonthlyPosts.objects.get(title="Title: 7"))
        
        qs = MonthlyPosts.objects.get(title="Title: 8")
        qs.set_post_to_display()
        qs.save()
        qs = MonthlyPosts.objects.get(title="Title: 4")
        qs.set_post_to_display()
        qs.save()
        
        mp = MonthlyPosts.objects.filter(to_display=True)
        self.assertEqual(len(mp), 1)
        self.assertEqual(mp[0], MonthlyPosts.objects.get(title="Title: 4"))
        
    def test_display_a_post(self):
        qs = MonthlyPosts.objects.get(title="Title: 7")
        qs.set_post_to_display()
        qs.save()
        
        self.client.post(reverse('login'), {'password_field' : 'carriespassword'}, follow=True)
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthly_post'], qs)
        
    def test_load_page_with_no_previous_post(self):
        posts = MonthlyPosts.objects.all()
        for post in posts:
            post.delete()
            post.save()
        
        self.client.post(reverse('login'), {'password_field' : 'carriespassword'}, follow=True)
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthly_post'].title, 'No post to display')
        
        post = MonthlyPosts.objects.create(title="Title: 1", text='This is the body of the post', publish_date = date(1994, 5, 9))
        post.set_post_to_display()
        post.save()
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['monthly_post'].title, 'Title: 1')
      
# ------ LINKS ------# 
    
class LinksTest(ccTestCase):
    
    
    def setUpData(self):
        for i in range(1, 6):
            Links.objects.create(
                title="Google {}".format(i), 
                description="this is a good place to search.  Its like, #{}".format(i), 
                url="https://www.google.com/search?q={}".format(i))
    
    
    def create_links(self):
        allLinks = Links.objects.all()
        self.assertEqual(len(allLinks), 5)
        
        self.attempt_login_with_password('carriespassword')
        


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    
