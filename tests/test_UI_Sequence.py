
from django.urls import reverse

from cc.models import MonthlyPosts

from .ccTestCases import ccIntegratedTestCase

class IntegratedTest(ccIntegratedTestCase):
    # The general structure is 'carrieUser' does something and then 'parent' verifies it.      

    def test_login(self):
        self.login('carriespassword')
        self.assertEqual('{0}{1}'.format(self.live_server_url, reverse('home')), self.selenium.current_url)  
        
        self.login('parentpassword') 
        self.assertEqual('{0}{1}'.format(self.live_server_url, reverse('home')), self.selenium.current_url)  
        
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
        
        self.assertEqual(MonthlyPosts.objects.count(), 2)
        # one for the previous, and one for the blank post that was created by 'new'. 
        
        self.scan_page_for(["blank title", "write something new"])
        
        post_header = self.selenium.find_element_by_id('monthly-header-form')
        post_text = self.selenium.find_element_by_id('monthly-text-form')
        post_submit = self.selenium.find_element_by_name('save')
        
        post_header.clear()
        post_text.clear()
        
        post_header.send_keys("tomatoes2")
        post_text.send_keys("pickles2")
        
        post_submit.click() 
        
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
        
        self.assertEqual(MonthlyPosts.objects.count(), 3)
        
        # --- parent ---
        
        self.login('parentpassword')
        
        self.scan_page_for(["tomatoes3", "pickles3"])
            
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
    