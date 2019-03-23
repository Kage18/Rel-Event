from django import forms
from .models import event
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):
    # invited_users = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=User.objects.all())
    class Meta:
        model = event
        fields = '__all__'
        exclude = ['user', 'registered_users']

    # def __init__(self, *args, **kwargs):
    #     super(EventForm, self).__init__(*args, **kwargs)
    #     self.fields['invited_users'] = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple,
    #                                                           queryset=User.objects.all(),
    #                                                           )

    def save(self, request, commit=True):
        f = super(EventForm, self).save(commit=True)
        f.user = request.user
        f.name = self.cleaned_data['name']
        f.description = self.cleaned_data['description']
        f.venue = self.cleaned_data['venue']
        f.city = self.cleaned_data['city']
        f.state = self.cleaned_data['state']
        f.private = self.cleaned_data['private']
        if self.cleaned_data['private'] == False:
            print(self.cleaned_data['private'],'hugvvuhbjgchcgcgkhhkchv')
            # f.invited_users.add(*self.cleaned_data['invited_users'])
        f.date = self.cleaned_data['date']
        f.time = self.cleaned_data['time']
        if commit:
            f.save()

        return f
