from django.contrib import admin

# Register your models here.

# from .models import Mymodel1
# from .models import DemoModel

# from .models import Announce
from .models import Contact
from .models import ContactGroup
from .models import Site
from .models import Service
#from .models import Incident
from .models import Info

# -----------------------
# class AnnounceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'visible','author','created_on')
#     list_filter = ("created_on","visible","author")
#     #search_fields = ['name','content']

# admin.site.register(Announce, AnnounceAdmin)

# -----------------------
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname','lastname','mobile','comment','is_active','want_sms','want_email','pk')
    list_filter = ("is_active","want_email","want_sms")


#admin.site.register(Contact)

@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    list_display =('name','description','size','pk')

# -----------------------
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'description')
    

# -----------------------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'description')

# -----------------------
# @admin.register(Incident)
# class IncidentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'status', 'priority','start','duration')
#     list_filter = ("priority","status")

# -----------------------
@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('category', 'pk','title', 'status', 'priority','start','duration','author','visible',
            'is_template')
    list_filter = ('category', 'priority','status','is_template','visible')
    radio_fields = {"category": admin.HORIZONTAL}
    save_on_top = True
    # fieldsets = (
    #     ('AAA', {'fields': ('title','status')}),
    #     ('BBB', {'fields': ('start','duration')})
    #     )
    # NOK sortable_by = ['pk']
