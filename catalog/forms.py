import datetime

from django.forms import ModelForm

from .models import BookInstance

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookModelForm(ModelForm):
    
    def clean_renewal_date(self):
        """Check if date is between now and 4 weeks."""
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal date in the past'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal date more than 4 weeks away.'))
        
        return data
    

    class Meta:
        model = BookInstance
        fields = ['due_back']
        label = {'due_back': _('Renewal Date')}
        help_text = {'due_back': _('Enter a date between now and 4 weeks(default 3 weeks).')}