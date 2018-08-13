from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from .models import Quest, Evaluation, Organizer
from django.conf import settings
from django.db.models.signals import post_save
from .models import Tag
from datetimewidget.widgets import DateTimeWidget, DateWidget


def post_save_receiver(sender, instance, created, **kwargs):
    pass


post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)


class QuestForm(forms.ModelForm):

    DISABLE_TYPE = [
        ('Vision', 'Vision'),
        ('Hearing', 'Hearing'),
        ('Walking', 'Walking'),
        ('Multiple Disabilities', 'Multiple Disabilities'),
        ('Other', 'Other'),
    ]

    title = forms.CharField(label='TITLE', max_length=50)
    type = forms.CharField(widget=forms.Select(choices=DISABLE_TYPE))
    intro = forms.CharField(label='INTRODUCTION', max_length=5000)
    abstract = forms.TextInput(attrs={'size': 5, 'maxlength': 5})
    #document = forms.FileField()
    tags = forms.CharField(label='Tags, separated by ","', max_length=50)

    options = []
    options[:] = []
    tags = Tag.objects.all()
    for tag in tags:
        options.insert(0, (tag, tag))

    tags = forms.MultipleChoiceField(label='Select Tags', widget=forms.CheckboxSelectMultiple, choices=options)

    class Meta:
        model = Quest
        #fields = ('title', 'intro', 'document', 'type', 'abstract', 'tags')
        fields = ('title', 'intro', 'type', 'abstract', 'tags')


class EvaluationForm(forms.ModelForm):
    evaluation = forms.FileField()

    class Meta:
        model = Evaluation
        fields = ('evaluation',)


class OrganizationForm(forms.ModelForm):
    Fields = [
        ('Vision', 'Vision'),
        ('Hearing', 'Hearing'),
        ('Walking', 'Walking'),
        ('Multiple Disabilities', 'Multiple Disabilities'),
        ('Other', 'Other'),
        ]

    title = forms.CharField(label='Title', max_length=50)
    type = forms.CharField(widget=forms.Select(choices=Fields), help_text='Please Select A Profession')
    description = forms.TextInput(attrs={'size': 5})
    scheduled_time = forms.DateTimeField(label='Scheduled Date', widget=DateTimeWidget(usel10n=True, bootstrap_version=2))

    class Meta:
        model = Organizer
        fields = ('title', 'type', 'description', 'scheduled_time')
        widgets = {
            'datetime': DateTimeWidget(attrs={'id': "yourdatetimeid"}, usel10n=True, bootstrap_version=2)
        }


class SignUpForm(UserCreationForm):
    Fields = [
        ('Vision', 'Vision'),
        ('Hearing', 'Hearing'),
        ('Walking', 'Walking'),
        ('Multiple Disabilities', 'Multiple Disabilities'),
        ('Other', 'Other'),

    ]

    Groups = [
        ('User', 'User'),
        ('Assistant', 'Assistant'),
        ('Organizer', 'Organizer'),
    ]

    type = forms.CharField(widget=forms.Select(choices=Fields), help_text='Please Select Your Profession')
    groups = forms.CharField(widget=forms.Select(choices=Groups), help_text='Note: Register as Chair needs Admin approval!')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'groups', 'type', 'email')

