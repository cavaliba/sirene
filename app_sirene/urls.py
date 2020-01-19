from django.urls import path
from django.views.generic import TemplateView

from .views import home
from .views import AboutView
# from .views import announce_list, announce_detail
from .views import contact_list
from .views import contact_group_list
from .views import contact_group_detail
from .views import site_list
from .views import service_list
#from .views import incident_detail
#from .views import incident_new
#from .views import incident_edit
from .views import info_list
from .views import info_detail
from .views import info_new
from .views import info_edit
from .views import template_list
from .views import notify_test
from .views import notify_confirm
from .views import notify_send

# provided by django AAA
# from myapp1.views import logout


# from myapp1.views import Mymodel1List, Mymodel1Detail, Mymodel1LastList
# from myapp1.views import Mymodel1Create, Mymodel1Update, Mymodel1Delete
#from myapp1.views import mymodel1_edit


# url namespace
app_name="app_sirene"

urlpatterns = [
    #path('', views.home, name='home'),
    path('', home, name='home'),

    path('about/', AboutView.as_view(), name='about'),
    #path('about/', TemplateView.as_view(template_name="myapp1/about.html"), name='about'),
    #path('', about, name='about'),
    #path('new/', TemplateView.as_view(template_name="app_sirene/new.html"), name='new'),

    # ----------------------------    
    # announce 
    # ----------------------------

    # path('announce_list/<str:myrange>/', announce_list, name='announce_list'),
    # path('announce_detail/<int:pk>/', announce_detail, name='announce_detail'),

    # ----------------------------
    # contact list
    # ----------------------------
    path('contact/', contact_list, name='contact_list'),
    path('group/', contact_group_list, name='contact_group_list'),
    path('group/<int:pk>/', contact_group_detail, name='contact_group_detail'),

    # --------------------------
    # Infos
    # --------------------------

    path('template/', template_list, name='template_list'),

    path('info/', info_list, name='info_list'),
    path('info/<int:pk>/', info_detail, name='info_detail'),
    path('info/new/', info_new, name='info_new'),
    path('info/new/<int:pk>/', info_new, name='info_new_from_template'),
    path('info/<int:pk>/edit', info_edit, name='info_edit'),

    # --------------------------
    # incident
    # --------------------------
    # list
    #path('incident/',
    #path('incident/?p=year',
    #path('incident/?p=all&site=MLV',
    #path('incident/new/', incident_new, name='incident_new'),
    #path('incident/<int:pk>/', incident_detail, name='incident_detail'),
    #path('incident/<int:pk>/edit', incident_edit, name='incident_edit'),

    # ----------------------------
    # site list
    # ----------------------------    
    path('site/', site_list, name='site_list'),

    # ----------------------------
    # service_list
    # ----------------------------    
    path('service/', service_list, name='service_list'),


    # ----------------------------
    # service_list
    # ----------------------------    
    path('notify_confirm/<int:pk>/', notify_confirm, name='notify_confirm'),
    path('notify_send/<int:pk>/', notify_send, name='notify_send'),
    path('notify_test/', notify_test, name='notify_test'),

    # logout
    # use Django app from global settings/urls (accounts/)
    # path('logout/', logout, name='logout'),
    #path('logout/', TemplateView.as_view(template_name="myapp1/logout.html"), name='logout'),

    # # Mymodel1
    # path('mymodel1/',          Mymodel1List.as_view(), name='mymodel1_list'),
    # path('mymodel1/<int:pk>/', Mymodel1Detail.as_view(), name='mymodel1_detail'),
    # path('mymodel1/last/',     Mymodel1LastList.as_view(), name='mymodel1_last_list'),
    
    # #path('mymodel1/edit/',     mymodel1_edit, name='mymodel1_edit'),  
    # path('mymodel1/edit/',                Mymodel1Create.as_view(), name='mymodel1_edit'),  
    # path('mymodel1/<int:pk>/edit/',       Mymodel1Update.as_view(), name='mymodel1_edit'),  
    # path('mymodel1/<int:pk>/delete/',     Mymodel1Delete.as_view(), name='mymodel1_delete'),  

]
