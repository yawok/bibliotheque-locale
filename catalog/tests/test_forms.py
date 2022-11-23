import datetime

from django.utils import timezone
from django.test import TestCase

from catalog.forms import RenewBookModelForm


class RenewBookModelFormTests(TestCase):
    
    def test_renewal_date_field_label(self):
        form = RenewBookModelForm()
        self.assertEqual(form.fields['due_back'].label, 'Renewal Date')

        
    def test_renewal_date_field_help_text(self):
        form = RenewBookModelForm()
        self.assertEqual(form.fields['due_back'].help_text, 'Enter a date between now and 4 weeks(default 3 weeks).')
        
     
    def test_renewal_form_date_in_the_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookModelForm({'due_back': date})
        self.assertFalse(form.is_valid()) 
        

    def test_renewal_form_date_too_far_in_the_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4, days=1)
        form = RenewBookModelForm({'due_back': date})
        self.assertFalse(form.is_valid()) 
               

    def test_renewal_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookModelForm({'due_back': date})
        self.assertTrue(form.is_valid())
        
        
    def test_renewal_form_max_date(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookModelForm({'due_back': date})
        self.assertTrue(form.is_valid())