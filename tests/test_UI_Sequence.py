
from django.urls import reverse

from cc.models import MonthlyPosts

from .ccTestCases import ccIntegratedTestCase

import time


class IntegratedTest(ccIntegratedTestCase):
    # The general structure is 'carrieUser' does something and then 'parent' verifies it.      

    def test_login(self):
        self.login('carriespassword')
        self.assertEqual('{0}{1}'.format(self.live_server_url, reverse('home')), self.selenium.current_url)  
        
        self.login('parentpassword') 
        self.assertEqual('{0}{1}'.format(self.live_server_url, reverse('home')), self.selenium.current_url)  
        
    # 'carrie' edits and saves a post, and a 'parent' verifies those changes. 
    def test_post(self):
        
        # --- carrie: edit ('save') ---
        
        self.login('carriespassword')
        self.scan_page_for(["No post", "like there"])
        
        self.create_post('tomatoes', 'pickles')
        self.scan_page_for(["tomatoes", "pickles"])
        
        # this was turning up in the 'source_code' without appearing on the page, so I am running a quick double check
        textarea = self.selenium.find_element_by_id('monthly-text-form')
        self.assertEqual(textarea.text, "pickles")
        
        # --- parent ---
        
        self.login('parentpassword')
        self.scan_page_for(["tomatoes", "pickles"])
        
        # --- carrie --- 'new'
        
        self.login('carriespassword')
        self.selenium.find_element_by_name("new").click()
     
        self.scan_page_for(["blank title", "write something new"])
        
        # one for the previous, and one for the blank post that was created by 'new'. 
        self.assertEqual(MonthlyPosts.objects.count(), 2)
        
        self.create_post('tomatoes2', 'pickles2')
        self.scan_page_for(["tomatoes2", "pickles2"])
        
        self.selenium.find_element_by_name("new").click()
        self.scan_page_for(["blank title", "write something new"])

        self.create_post('tomatoes3', 'pickles3')
        self.scan_page_for(["tomatoes3", "pickles3"])
        
        # tomatoes and pickles: 1, 2 & 3
        self.assertEqual(MonthlyPosts.objects.count(), 3)
        
        # --- parent ---
        
        self.login('parentpassword')
        self.scan_page_for(["tomatoes3", "pickles3"])
        
    def create_post(self, header, text):
        self.clear_fields( [('id', 'monthly-header-form'), ('id','monthly-text-form')] )
        self.populate_fields( [('id', 'monthly-header-form', header), ('id', 'monthly-text-form', text)] )
        self.selenium.find_element_by_name('save').click()
        
    #Takes list of tuples with the element's type and name, and clears them.
    def clear_fields(self, type_and_name_list, root_xpath=""):
        for type_and_name in type_and_name_list:
            elm_type = type_and_name[0]
            name = type_and_name[1]
            
            if root_xpath != "":
                self.selenium.find_element_by_xpath("{}//*[contains(@{}, '{}')]".format(root_xpath, elm_type, name)).clear() 
                continue     
            
            if elm_type == 'id':
                self.selenium.find_element_by_id(name).clear()
            if elm_type == 'class':
                self.selenium.find_element_by_class_name(name).clear()
            if elm_type == 'name':
                self.selenium.find_element_by_name(name).clear()
                
    def populate_fields(self, type_name_text_list, root_xpath=""):
        for type_name_text in type_name_text_list:
            elm_type = type_name_text[0]
            name = type_name_text[1]
            text = type_name_text[2]
            
            if root_xpath != "":
                self.selenium.find_element_by_xpath("{}//*[contains(@{}, '{}')]".format(root_xpath, elm_type, name)).send_keys(text)
                continue   
            
            if elm_type == 'id':
                self.selenium.find_element_by_id(name).send_keys(text)
            if elm_type == 'class':
                self.selenium.find_element_by_class_name(name).send_keys(text)
            if elm_type == 'name':
                self.selenium.find_element_by_name(name).clear().send_keys(text)  
            
           
    # this could be more efficient by modifying populate_fields() to clear the field before populating it.  
    def clear_and_populate_fields(self, type_name_text_list, root_xpath=""):
        self.clear_fields(type_name_text_list, root_xpath)
        self.populate_fields(type_name_text_list, root_xpath)
            
    def test_links(self):
        
        self.login('carriespassword')
        
        self.selenium.find_element_by_name('links_lnk').click()
        self.scan_page_for(["Dylan was here"])
        
        self.clear_and_populate_fields([
            ('class', 'link-title-form', 'Party City 1'), 
            ('class', 'link-description-form', 'Great place for loonies.'), 
            ('class', 'link-url-form', 'https://www.party-city.com')])
        
        self.selenium.find_element_by_name('save').click()
        self.scan_page_for(["loonies", "Party "])
        
        self.selenium.find_element_by_name('new').click()
        
        self.scan_page_for(["Dylan was here"])
        
        self.clear_and_populate_fields([
            ('class', 'link-title-form', 'Party City 2'), 
            ('class', 'link-description-form', 'Great place for loonies.'), 
            ('class', 'link-url-form', 'https://www.party-city2.com')], root_xpath="//*[@class='link-object']/form")
        
        self.selenium.find_element_by_name('save').click()
        self.selenium.find_element_by_name('new').click()
        
        self.clear_and_populate_fields([
            ('class', 'link-title-form', 'Party City 3'), 
            ('class', 'link-description-form', 'Great place for loonies.'), 
            ('class', 'link-url-form', 'https://www.party-city3.com')], root_xpath="//*[@class='link-object']/form")

        self.selenium.find_element_by_name("save").click()
        
        self.scan_page_for(["Party City 2", "Party City 1", "Party City 3"])
        
        self.selenium.find_element_by_name('delete').click()
        
        self.scan_page_for(["Party City 1"], booli=False)
        
        self.login("parentpassword")
        
        self.selenium.find_element_by_name('links_lnk').click()
        
        time.sleep(5)
        
        self.scan_page_for(["Party City 2", "Party City 3"])
        
        self.login('carriespassword')
        
        self.selenium.find_element_by_name("links_lnk").click()
        
        self.clear_and_populate_fields([
            ('class', 'link-title-form', 'Party City 2 Edit'), 
            ('class', 'link-description-form', 'Great place for loonies. Edit'), 
            ('class', 'link-url-form', 'https://www.party-city2.com')], root_xpath="//*[@class='link-object']/form")
        
        self.selenium.find_element_by_name('save').click()
        
        self.scan_page_for(["Party City 2 Edit"])
        
        self.selenium.find_element_by_name('save').click()
        self.selenium.find_element_by_name('new').click()
        
        self.login('parentpassword')
        
        self.selenium.find_element_by_name("links_lnk").click()
        
        self.scan_page_for(["Dylan was here"], booli=False)
        
    
        
        
    