from .ccTestCases import ccTestCase

from datetime import date

from django.urls import reverse

from cc.models import MonthlyPosts


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
        postCount = MonthlyPosts.objects.count()
        MonthlyPosts.objects.get(title="Title: 5").delete()
        self.assertEquals(MonthlyPosts.objects.count(), postCount-1)
        
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