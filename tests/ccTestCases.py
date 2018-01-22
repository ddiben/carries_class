
from django.contrib.auth.models import User
from django.urls import reverse

from django.test import TestCase
from django.test.client import RequestFactory

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class ccTestCase(TestCase):
    
    @classmethod
    def setUp(cls):
        cls.factory = RequestFactory()
        
        User.objects.create_user(username='carrieUser', email="carrie@notmail.com", password='carriespassword')
        User.objects.create_user(username='parent', email="parent@notmail.com", password='parentpassword')
        
    def login(self, password):
        response = self.client.post(reverse('login'), {'password_field' : password}, follow=True)
        self.assertIsNotNone(response.context)
        self.assertTrue(response.context['user'].is_authenticated())
    
    def queryset_contains(self, obj_to_search_for, queryset):
        for query_object in queryset:
            if query_object.__str__() == obj_to_search_for.__str__():
                return True
        return False
        
        
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
        self.selenium.get('%s%s' % (self.live_server_url, reverse('login')))
        password_input = self.selenium.find_element_by_class_name('login-input')
        password_input.send_keys(password)
        self.selenium.find_element_by_class_name('login-submit').click()
        
    def scan_page_for(self, listOfStrings, booli=True):
        page = self.selenium.page_source
        for search_string in listOfStrings:
            if booli == True:
                self.assertTrue(search_string in page, "Unable to locate: '{}'".format(search_string))
            if booli == False:
                self.assertFalse(search_string in page, "Able to locate: '{}'".format(search_string))
            
        