
from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class ccTestCase(TestCase):
    
    def setUp(self):
        
        User.objects.create_user(username='carrieUser', email="carrie@notmail.com", password='carriespassword')
        User.objects.create_user(username='parent', email="parent@notmail.com", password='parentpassword')
    
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
        
class ccIntegratedTestCase(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome('/usr/local/bin/chromedriver')
        cls.selenium.implicitly_wait(5)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        
    def setUp(self):
        User.objects.create_user(username='carrieUser', password='carriespassword')
        User.objects.create_user(username='parent', password='parentpassword')
        
    def login(self, password):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        password_input = self.selenium.find_element_by_class_name('login-input')
        password_input.send_keys(password)
        self.selenium.find_element_by_class_name('login-submit').click()
        
    def scan_page_for(self, listOfStrings):
        page = self.selenium.page_source
        for search_string in listOfStrings:
            assert search_string in page