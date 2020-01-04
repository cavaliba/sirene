# views.py

import datetime
import re


from django.conf import settings

from django.utils import timezone
from django.db.models import Q

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.urls import reverse_lazy

from django.views import View
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import get_object_or_404

# manual templates
# from django.template.loader import get_template
# from django.template import Context
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# from .models import Announce
from .models import Contact
from .models import ContactGroup
from .models import Site
from .models import Service
# from .models import Incident
from .models import Info

from .forms import InfoForm

# --------------------------------------------------------
# Send Notifications - email - sms
# --------------------------------------------------------
def send_sms(num,sms):
    # TODO - plug external API here
    print("send_sms() ; from:",num," ; content:",sms[0:5],"(...)")
    return True


def send_notification(ninf):
    """Send all noticications required from Info object ninf"""

    result = True

    # build a list of emails and sms
    emails={}
    sms={}

    for grp in ninf.notify_groups.all():
        #print("Group:",grp)
        for contact in grp.contacts.all():
            #print("   Contact:",contact)
            if contact.is_active:
                if contact.want_email:
                    emails[contact.email]=1
                if contact.want_sms:
                    sms[contact.mobile]=1

    # emails
    # ------
    if ninf.visible and ninf.send_email:
        # d = Context({'info': ninf })
        # plaintext = get_template('sirene_email.txt')
        # text_content = plaintext.render(d)
        # htmly     = get_template('app_sirene/email.html')
        # html_content = htmly.render(d)
        text_content = render_to_string('app_sirene/email.txt', {'info': ninf})
        html_content = render_to_string('app_sirene/email.html', {'info': ninf})
        #subject = ninf.title
        from_email = settings.SIRENE_EMAIL_FROM
        subject = settings.SIRENE_EMAIL_SUBJECT

        all_messages=[]
        for dest in emails.keys():
            msg = mail.EmailMultiAlternatives(subject, text_content, from_email, [dest])
            msg.attach_alternative(html_content, "text/html")
            #msg = mail.EmailMessage(subject=subject, from_email=from_email, body=html_content, to=[dest])
            #msg.content_subtype = "html"  # Main content is now text/html
            #msg.send()
            all_messages.append(msg)

        try:
            connection = mail.get_connection()
            connection.send_messages(all_messages)
            connection.close()
        except:
            result=False
  
    # SMS
    # ---
    if ninf.visible and ninf.send_sms:
        sms_content = render_to_string('app_sirene/sms.txt', {'info': ninf})
        for dest in sms.keys():
            if not send_sms(dest,sms_content):
                result = False

    return result

# --------------------------------------------------------
# NOTIFY TEST
# --------------------------------------------------------

@login_required
def notify_test(request):
    #return HttpResponse("Hello from notify_test")

    # GET - send empty form
    if request.method =='GET':
        return render(request, 'app_sirene/notify_test.html',{})
    
    # POST - process form
    # print (request.POST)
    if 'email' in request.POST:
        dirty_email = request.POST['email']
        if re.match(r'^[^@]+@[^@]+\.[^@]+', dirty_email):
            clean_email=dirty_email
        else:
            messages.add_message(request, messages.ERROR, "Format d'adresse EMAIL invalide")
            return render(request, 'app_sirene/notify_test.html',{})

        text_content = render_to_string('app_sirene/email_test.txt', {})
        html_content = render_to_string('app_sirene/email_test.html', {})

        from_email = settings.SIRENE_EMAIL_TEST_FROM
        subject = settings.SIRENE_EMAIL_TEST_SUBJECT

        try:
            msg = mail.EmailMultiAlternatives(subject, text_content, from_email, [clean_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.add_message(request, messages.SUCCESS, 'Envoi de MAIL réussi.')
        except:
            messages.add_message(request, messages.ERROR, 'Envoi de MAIL échoué.')



    if 'sms' in request.POST:
        dirty_sms = request.POST['sms']

        if re.match(r'^^\d{10}$', dirty_sms):
        #if re.match(r'^^\+?1?\d{9,15}$', dirty_sms):
            clean_num=dirty_sms
        else:
            messages.add_message(request, messages.ERROR, 'Format de numéro SMS invalide (10 chiffres).')
            return render(request, 'app_sirene/notify_test.html',{})

        sms = render_to_string('app_sirene/sms_test.txt', {})    
        try:
            send_sms(clean_num,sms)
            messages.add_message(request, messages.SUCCESS, 'Envoi de SMS réussi.')
        except:
            messages.add_message(request, messages.ERROR, 'Envoi de SMS échoué.')


    #return HttpResponse("Hello from notify_test")
    return render(request, 'app_sirene/notify_test.html',{})

# --------------------------------------------------------
# HOME PAGE
# --------------------------------------------------------

#@login_required
def home(request):

    lastweek = timezone.now() - datetime.timedelta(days=7)
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    incidents = Info.objects.filter(category=1).filter(visible=True).filter(is_template=False)\
        .filter(status=2).order_by('priority')

    maintenances = Info.objects.filter(category=2).filter(visible=True).filter(is_template=False)\
        .filter( Q(start__gte=today) | Q(status__lte=2)).order_by('start')
        #.filter(start__gte=today).filter(status__lte=2).order_by('priority')

    announces = Info.objects.filter(category=3).filter(visible=True).filter(is_template=False)\
        .filter(start__gte=lastweek).filter(status__lte=2).order_by('-start')

    context = {
        'maintenances': maintenances,
        'announces': announces,
        'incidents': incidents,
    }
    return render(request, 'app_sirene/home.html',context)

# --------------------------------------------------------
# template/
# --------------------------------------------------------
# display list of templates, with link to create new event
@login_required
def template_list(request):

    templates = Info.objects.filter(visible=True).filter(is_template=True)\
            .order_by('category','template_name')
    return render(request, 'app_sirene/template_list.html',{'templates' : templates})


# --------------------------------------------------------
# Info
# --------------------------------------------------------

# info/
def info_list(request):
    #return HttpResponse("Hello from info_list")

    # infos = Info.objects.filter(created_on__gte=mytmp).filter(visible=True).order_by('-created_on')

    raw = Info.objects.filter(visible=True).filter(is_template=False).order_by('-start')

    myweek = timezone.now() - datetime.timedelta(days=7)
    mymonth = timezone.now() - datetime.timedelta(days=30)
    myyear = timezone.now() - datetime.timedelta(days=365)

    # my_param = request.GET.get('param')
    # if my_param is None:
    #     return HttpResponseBadRequest()

    # filter_arguments = {query: x}
    # some_model.filter(**filter_arguments)

    # x = AnswerModel.objects.filter(Q(user='tim') | Q(user='paul') | Q(question='i like jam')
    # for query in query_string.split(' '): # split search words
    #     for field in fields:
    #          argument_list.append( Q(**{field+'__icontains': query} )
    # # join the arguments in the list with the or operator
    # query = MyModel.objects.filter(  reduce(operator.or_, argument_list)  ) 


    myrange = request.GET.get('r', 'all')
    if myrange == "year":
        range_filter= Info.objects.filter(start__gte=myyear)
    elif myrange == "month":
        range_filter=Info.objects.filter(start__gte=mymonth)
    elif myrange == "week":
        range_filter=Info.objects.filter(start__gte=myweek)
    else:
        range_filter = raw

    mycat = request.GET.get('c', 'all')
    if mycat == "i":
        cat_filter= Info.objects.filter(category=1)
    elif mycat == "m":
        cat_filter=Info.objects.filter(category=2)
    elif mycat == "a":
        cat_filter=Info.objects.filter(category=3)
    else:
        cat_filter = raw

    infos = raw & cat_filter & range_filter

    return render(request, 'app_sirene/info_list.html',{'infos' : infos})


# ------------------
# info/<int>/
def info_detail(request, pk):
   #return HttpResponse("Hello from Info Detail : " + str(pk))
    pk=int(pk)

    try:
        info = Info.objects.filter(is_template=False).filter(visible=True).get(pk=pk)
    except:
        raise Http404("Aucun événement correspondant.")

    return render(request, 'app_sirene/info_detail.html',{ 'info':info })

# -------------------------------------------
# info/new/ ; no id   or <pk> as template id
@login_required
def info_new(request, pk=None):

    # POST : submitted form ; check and create
    if request.method == 'POST':

        form = InfoForm(request.POST)

        if form.is_valid():
            #return HttpResponseRedirect('app_sirene/home.html')
            # insert into database from cleaned_data
            ninf = Info()
            ninf.category   = form.cleaned_data['category']
            ninf.title      = form.cleaned_data['title']
            ninf.status     = form.cleaned_data['status']
            ninf.priority   = form.cleaned_data['priority']
            ninf.start      = form.cleaned_data['start']
            ninf.duration   = form.cleaned_data['duration']
            ninf.downtime   = form.cleaned_data['downtime']
            ninf.detail     = form.cleaned_data['detail']
            ninf.send_email = form.cleaned_data['send_email']
            ninf.send_sms   = form.cleaned_data['send_sms']
            ninf.author     = form.cleaned_data['author']
            # save here to get an ID needed before add many2many items
            try:
                ninf.save()
                messages.add_message(request, messages.SUCCESS, 'Evénement enregistré.')
            except:
                messages.add_message(request, messages.ERROR, "Erreur d'enregistrement.")

            # sites
            for item in form.cleaned_data['sites']:
              ninf.sites.add(item)
            # services
            for item in form.cleaned_data['services']:
              ninf.services.add(item)
            # notif groups
            for item in form.cleaned_data['notify_groups']:
              ninf.notify_groups.add(item)

            ninf.save()

            # send notifications
            if send_notification(ninf):
                messages.add_message(request, messages.SUCCESS, 'Envoi de MAIL/SMS réussi.')
            else:
                messages.add_message(request, messages.ERROR, 'Envoi de MAIL/SMS échoué.')

            return HttpResponseRedirect(reverse('app_sirene:home'))
       

    # GET - new form - empty or template-based ?
    else:
        if pk is None:
            # new empty form if no pk given
            form = InfoForm()
        else:
            # from template 
            queryset=Info.objects.filter(visible=True).filter(is_template=True)
            ninf = get_object_or_404(queryset,pk=pk)
            # reset specific value
            ninf.is_template = False
            ninf.author = ""
            ninf.start = timezone.now()
            form = InfoForm(instance = ninf)
            #form.fields["is_template"].initial = False

    # form not valid : resend
    return render(request, 'app_sirene/info_form.html', {'form': form})

# -----------------
# info/<int>/edit   ; and close ...
@login_required
def info_edit(request, pk):

    try:
        ninf = Info.objects.get(pk=pk)
    except:
        raise Http404("Evénement non disponible.")

    form = InfoForm(data=request.POST or None, instance = ninf)

    if request.method == 'POST':    
        if form.is_valid():
            ninf.category    = form.cleaned_data['category']
            ninf.title       = form.cleaned_data['title']
            ninf.status      = form.cleaned_data['status']
            ninf.priority    = form.cleaned_data['priority']
            ninf.start       = form.cleaned_data['start']
            ninf.duration    = form.cleaned_data['duration']
            ninf.downtime    = form.cleaned_data['downtime']
            ninf.detail      = form.cleaned_data['detail']
            ninf.send_email  = form.cleaned_data['send_email']
            ninf.send_sms    = form.cleaned_data['send_sms']
            ninf.downtime    = form.cleaned_data['downtime']
            ninf.author      = form.cleaned_data['author']
            ninf.sites.set(form.cleaned_data['sites'])
            ninf.services.set(form.cleaned_data['services'])
            ninf.notify_groups.set(form.cleaned_data['notify_groups'])

            try:
                ninf.save()
                messages.add_message(request, messages.SUCCESS, 'Evénement enregistré.')
            except:
                messages.add_message(request, messages.ERROR, "Erreur d'enregistrement.")

            # send notifications
            if send_notification(ninf):
                messages.add_message(request, messages.SUCCESS, 'Envoi de MAIL/SMS réussi.')
            else:
                messages.add_message(request, messages.ERROR, 'Envoi de MAIL/SMS échoué.')

            return HttpResponseRedirect(reverse('app_sirene:home'))

        else:
            messages.add_message(request, messages.ERROR, 'Formulaire invalide.')

    return render(request, 'app_sirene/info_form.html', {'form': form})

# --------------------------------------------------------
# Contact, Group
# --------------------------------------------------------

@login_required
def contact_list(request):
    #return HttpResponse("Hello from Contact List")
    contacts = Contact.objects.all() 
    context = {
        'contacts': contacts,
    }
    return render(request, 'app_sirene/contact_list.html',context)

@login_required
def contact_group_list(request):
    #return HttpResponse("Hello from Contact List")
    contactgroups = ContactGroup.objects.all() 
    context = {
        'contactgroups': contactgroups,
    }
    return render(request, 'app_sirene/contact_group_list.html',context)

@login_required
def contact_group_detail(request, pk):
   pk=int(pk)
   contactgroup = ContactGroup.objects.get(pk=pk)
   context = {
        'contactgroup': contactgroup,
    }
   return render(request, 'app_sirene/contact_group_detail.html',context)
 

# --------------------------------------------------------
# Site
# --------------------------------------------------------

@login_required
def site_list(request):
    #return HttpResponse("Hello from Site List")
    sites = Site.objects.all() 
    context = { 'sites': sites, }
    return render(request, 'app_sirene/site_list.html',context)
    
# --------------------------------------------------------
# Service
# --------------------------------------------------------

@login_required
def service_list(request):
    #return HttpResponse("Hello from Service List")
    services = Service.objects.all() 
    context = { 'services': services, }
    return render(request, 'app_sirene/service_list.html',context)


# --------------------------------------------------------
# About
# --------------------------------------------------------

class AboutView(generic.TemplateView):
#class AboutView(LoginRequiredMixin, generic.TemplateView):
# #     # inherit from TemplateView and set specific template_name
# #     # for direct use in urls.py with
# #     #    path('about/', AboutView.as_view(), name='about'),
    template_name = "app_sirene/about.html"


