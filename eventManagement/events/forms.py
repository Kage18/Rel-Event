# from django import forms
# from .models import event,invitation,comment
# from django.contrib.auth.models import User
#
#
# class EventForm(forms.ModelForm):
#     CHOICES = [[x.id, x.username] for x in User.objects.all()]
#     invite_users = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=CHOICES)
#     message=forms.CharField(max_length=100)
#
#     class Meta:
#         model = event
#         fields = '__all__'
#         exclude = ['user', 'registered_users',]
#
#
#
#     def save(self, request, commit=True):
#
#         f = super(EventForm, self).save(commit=True)
#         f.user = request.user
#         f.name = self.cleaned_data['name']
#         f.description = self.cleaned_data['description']
#         f.venue = self.cleaned_data['venue']
#         f.city = self.cleaned_data['city']
#         f.state = self.cleaned_data['state']
#         f.private = self.cleaned_data['private']
#         f.date = self.cleaned_data['date']
#         f.time = self.cleaned_data['time']
#         if commit:
#             f.save()
#
#         return f
#
#
#
# class CommentForm(forms.ModelForm):
#
#
#     class Meta:
#         model = comment
#         fields = '__all__'
#         exclude = ['by']
