# forms.py
# (c) Cavaliba - 2019


from django import forms
from django.forms import ModelForm

from .models import Info
from .models import INFO_CATEGORY



# ----------------------------------------------------------
# Incidents
# ----------------------------------------------------------

# create Form from Model
class InfoForm(ModelForm):
    class Meta:
        model = Info
        fields = [ 'category', 'title','status', 'priority', 'author',
                'start','duration','downtime',
                'detail',
                'services','sites',
                'notify_groups','send_email', 'send_sms',
                'is_template','template_name',
                'visible',
        ]

        widgets = {
            'detail': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
             # Textarea
            #'start': forms.SelectDateWidget(),
            'sites': forms.SelectMultiple(attrs={'size': 8}),
            'services': forms.SelectMultiple(attrs={'size': 8}),
            'notify_groups': forms.SelectMultiple(attrs={'size': 8}),  
            #'category': forms.RadioSelect(attrs={'choices':INFO_CATEGORY}),
        }

# create Form manually
# class IncidentForm(forms.Form):
#     title = forms.CharField(label='Titre', max_length=100)



# ----------------------------------------------

# class Mymodel1Form(ModelForm):
#     class Meta:
#         model = Mymodel1
#         fields = ['name', 'amount', 'date','status']
#         # fields = '__all__'
#         # exclude = ['title']
#         # widgets = {
#         #     'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#         # }
#         # labels = {
#         #     'name': _('Writer'),
#         # }
#         # help_texts = {
#         #     'name': _('Some useful help text.'),
#         # }
#         # error_messages = {
#         #     'name': {
#         #         'max_length': _("This writer's name is too long."),
#         #     },
#         # }
#         # field_classes = {
#         #     'slug': MySlugFormField,
#         # }
#         localized_fields = ('date',)

