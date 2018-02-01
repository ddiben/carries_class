from __future__ import unicode_literals

from .ccTestCases import ccTestCase

from cc.models import Links
from cc.views import links

from django.urls import reverse

# testing the view
class LinksViewTest(ccTestCase):
    
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 6):
            Links.objects.create(
                title="Google {}".format(i), 
                description="this is a good place to search.  Its like, #{}".format(i), 
                url="https://www.google.com/search?q={}".format(i))
            
    def test_links_load(self):
        self.login('parentpassword')
        
        link4 = Links.objects.get(title="Google 4")
        
        response = self.client.get(reverse('links'))
        links = response.context['links']
        self.assertTrue(self.queryset_contains(link4, links))
        
        self.login('carriespassword')
        
        response = self.client.get(reverse('links'))
        links = response.context['links']
        self.assertTrue(self.queryset_contains(link4, links))
    
        
    # deleted links shouldn't show up
    def test_delete_link(self):
        self.login('carriespassword')
        
        link_del = Links.objects.get(title="Google 4").delete()
        
        response = self.client.get(reverse('links'))
        
        links = response.context['links']
        self.assertEqual(len(links), 4)
        self.assertFalse(self.queryset_contains(link_del, links))
        
    def test_no_links(self):
        self.login('parentpassword')
        
        allLinks = Links.objects.all()
        for link in allLinks:
            link.delete()
            
        self.assertEqual(Links.objects.count(), 0)
            
        response = self.client.get(reverse('links'))
        link = response.context['links']
        self.assertEqual(link[0].title, "No Links")
        
        self.login('carriespassword')
        response = self.client.get(reverse('links'))
        link = response.context['links']
        self.assertEqual(link[0].title, "Carrie's Class")
        
    def test_link_forms(self):
        self.login('carriespassword')
        
        response = self.client.get(reverse('links'))
        forms = response.context['forms']
        links = Links.objects.all()
        
        self.assertEqual(len(forms), len(links))

# testing the model
class LinksTest(ccTestCase):
    
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 6):
            Links.objects.create(
                title="Google {}".format(i), 
                description="this is a good place to search.  Its like, #{}".format(i), 
                url="https://www.google.com/search?q={}".format(i))
    
    def test_create_link(self):
        allLinks = Links.objects.all()
        self.assertEqual(len(allLinks), 5)
        
        test_url = "https://wwww.google.com/search?q=11"
        Links.objects.create(title="Google 11", description="I made this as a test", url=test_url)
        
        self.assertEqual(Links.objects.get(url=test_url).title, "Google 11")
        self.assertEqual(Links.objects.count(), 6)
        
    def test_edit_link(self):
        link_to_edit = Links.objects.get(title="Google 4")
        link_to_edit.description = "this is a different description."
        link_to_edit.save()
        
        self.assertEqual(Links.objects.get(title="Google 4").description, "this is a different description.")
        
    def test_delete_link(self):
        linkCount = Links.objects.count()
        Links.objects.get(title="Google 1").delete()
        self.assertEqual(Links.objects.count(), linkCount-1)
    