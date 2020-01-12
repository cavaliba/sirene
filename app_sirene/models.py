# models.py
# cavaliba.app_sirene
# (C) Cavaliba - 2020

import datetime
from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.forms import ModelForm


# null : DB
# blank : forms
# char/text : null=False


# -------------------------------------------------------------
# Contacts
# -------------------------------------------------------------

class Contact(models.Model):
    email     = models.CharField('Email', max_length=128, blank=False)
    mobile    = models.CharField('GSM', max_length=15, blank=False)
    firstname = models.CharField('Prenom', max_length=128, blank=True)
    lastname  = models.CharField('Nom', max_length=128, blank=True)
    is_active = models.BooleanField('Actif', default=True)
    want_email= models.BooleanField('Email', default=True)
    want_sms  = models.BooleanField('SMS', default=True)
    site      = models.CharField('Site', max_length=128, blank=True)

    class Meta:
        ordering = ['pk','lastname','firstname']

    def __str__(self):
        return self.email


class ContactGroup(models.Model):
    name        = models.CharField('Name', max_length=128, blank=False)
    description = models.TextField('Description', max_length=300, blank=True)
    contacts    = models.ManyToManyField(Contact, blank=True)
    
    class Meta:
        ordering = ['name']

    def size(self):
        return self.contacts.count()

    def __str__(self):
        return self.name


# -------------------------------------------------------------
# Site
# -------------------------------------------------------------

class Site(models.Model):
    name        = models.CharField('Label', max_length=32, blank=False)
    description = models.CharField('Description', max_length=128, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ' (' + self.description + ')'

# -------------------------------------------------------------
# Service
# -------------------------------------------------------------

class Service(models.Model):
    name        = models.CharField('Label', max_length=64, blank=False)
    description = models.CharField('Description', max_length=128, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ' (' + self.description + ')'


# -------------------------------------------------------------
# Info
# -------------------------------------------------------------

INFO_CATEGORY = (
     (0, "N/A"),
     (1, "Incident"),
     (2, "Maintenance"),
     (3, "Information"),
)


INFO_STATUS = (
     (0, "N/A"),
     (1, "Planifié"),
     (2, "En cours"),
     (3, "Terminé"),
)

INFO_PRIORITY = (
     (0,"N/A"),
     (1,"P1 - Critique"),
     (2,"P2 - Haute"),
     (3,"P3 - Moyenne"),
     (4,"P4 - Faible"),    
)

class Info(models.Model):
    category = models.IntegerField('Catégorie', choices=INFO_CATEGORY, default=1)
    title    = models.CharField('Titre', max_length=120, blank=False)
    status   = models.IntegerField('Etat', choices=INFO_STATUS, default=2)
    priority = models.IntegerField('Priorité', choices=INFO_PRIORITY, default=0)
    start    = models.DateTimeField('Début', blank=False, default=datetime.now,
                help_text="Format : dd/mm/YYYY hh:mm:ss")
    duration = models.IntegerField('Durée', default=0, blank=True, null=True,
            help_text="Durée estimée/définitive en minutes.")
    downtime = models.IntegerField('Indisponibilité', default=0, blank=True, null=True,
            help_text="Indisponibilité estimée/définitive en minutes.")
    detail   = models.TextField('Description', max_length=4000, blank=True, null=True)
    services = models.ManyToManyField(Service, blank=True)
    sites    = models.ManyToManyField(Site, blank=True)
    # notifications
    notify_groups = models.ManyToManyField(ContactGroup, blank=True)
    send_email    = models.BooleanField('Envoi de mail', default=True)
    send_sms      = models.BooleanField('Envoi de SMS', default=False)
    # template
    is_template   = models.BooleanField('Modèle', default=False)
    template_name = models.CharField('Nom de modele', max_length=120, blank=True)
    # meta
    author      = models.CharField('Auteur', max_length=200, blank=False,
             help_text="Saisir ici l'identité du déclarant de l'événement.")
    visible     = models.BooleanField('Visible', default=True)
    # created_on  = models.DateTimeField('Création', auto_now_add=True)
    # updated_on  = models.DateTimeField('Mise à jour', auto_now_add=True)
    created_on  = models.DateTimeField('Création',editable=False)
    updated_on  = models.DateTimeField('Mise à jour',editable=False)


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()
        return super(Info, self).save(*args, **kwargs)


    class Meta:
        ordering = ['start', 'priority', 'category']

    def __str__(self):
        return self.title

