
from .ccTestCases import ccTestCase

from cc.models import Links


class LinksTest(ccTestCase):
    
    def setUpTestData(self):
        for i in range(1, 6):
            Links.objects.create(
                title="Google {}".format(i), 
                description="this is a good place to search.  Its like, #{}".format(i), 
                url="https://www.google.com/search?q={}".format(i))
    
    def create_links(self):
        allLinks = Links.objects.all()
        self.assertEqual(len(allLinks), 5)
        
        self.attempt_login_with_password('carriespassword')