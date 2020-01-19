# fake_data.py
# (c) Cavaliba 2020

# create fake demo data for Cavaliba SIRENE


CONTACT = 20
CONTACTGROUP = 10
CONTACTGROUPSIZE = 5

import random
from random import randint

import faker

from app_sirene.models import Contact
from app_sirene.models import ContactGroup


f=faker.Faker('fr_FR')

# -------------------------
# Contact
# -------------------------
list_contact=[]

for i in range(CONTACT):

    c = Contact()
    c.email = f.company_email()
    c.mobile = f.msisdn()[:10]
    c.firstname = f.first_name()
    c.lastname = f.last_name()
    c.is_active = random.choice([True, False])
    c.want_sms = random.choice([True, False])
    c.want_email = random.choice([True, False])
    c.comment = f.job()


    c.save()
    list_contact.append(c)
    print(c.pk,c.email, c.mobile)

# -------------------------
# ContactGroup
# -------------------------
print()
for i in range(CONTACTGROUP):
    c = ContactGroup()

    c.name = 'GRP_' + f.last_name()
    c.description = f.text(max_nb_chars=40)

    c.save()

    for i in range(CONTACTGROUPSIZE):
        p=random.choice(list_contact)
        c.contacts.add(p)

    c.save()
    print(c.name, c.description)


