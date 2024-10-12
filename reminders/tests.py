from django.test import TestCase
from django.test import TestCase
from django.urls import reverse

class MyViewTests(TestCase):
    def test_redirect(self):
        response = self.client.get(reverse('views.reminder_set'))
        self.assertRedirects(response, '/reminder-set/') 
# Create your tests here.
