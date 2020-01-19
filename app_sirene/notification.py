# notification.py
# Cavaliba SIRENE (c) 2020

import re
from django.conf import settings

from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


import requests

# ----------------------------------------------------------------------------
def sirene_send_sms(num,sms):
    #
    #
    #
    # TODO - plug external API here
    #
    # check SMS number format
    if not re.match(r'^^\d{10}$', num):
    #if not re.match(r'^^\+?1?\d{9,15}$', sms):
        return False
  
    # ---------------------
    # 123-SMS / clic-secure
    # ---------------------
    # https://www.clic-secure.com/http.php?email=&pass=&numero=&message=
    login = settings.SMS_CONFIG['login']
    password = settings.SMS_CONFIG['password']
    test_only="test=o&"
    if settings.SMS_CONFIG['test_only'] == "no":
        test_only=""
    query = "https://www.clic-secure.com/http.php?{}email={}&pass={}&numero={}&message={}".format(
        test_only,
        login,
        password,
        num,
        sms,
        )
    print("SMS:QUERY:",query)
    r = requests.get(query)
    print("SMS:RESPONSE:", r.status_code, r.text)
    
            # a 80 : Le message a été envoyé
            # a 81 : Le message est enregistré pour un envoi en différé
            # r 82 : Le login et/ou mot de passe n’est pas valide
            # r 83 : vous devez créditer le compte
            # r 84 : le numéro de gsm n’est pas valide
            # r 85 : le format d’envoi en différé n’est pas valide
            # r 86 : le groupe de contacts est vide
            # r 87 : la valeur email est vide
            # r 88 : la valeur pass est vide
            # r 89 : la valeur numero est vide
            # r 90 : la valeur message est vide
            # r 91 : le message a déjà été envoyé à ce numéro dans les 24
            # dernières heures
            # (L’erreur 91 peut être désactivée dans la rubrique « Modifier les
            # options »)
            # a 92 le test d’envoi «à blanc» est positif
            # r 93 pour effectuer l’envoi de SMS vers les DOM TOM, vous
            # devez activer l’option (14) dans l’espace client
            # a 94 votre envoi en différé est supprimé
            # r 95 votre envoi en différé n’a pas pu être supprimé
            # r 96 votre adresse IP n’est pas valide
            # r 97 le SENDER ID n’est pas valide
            # r 98 la date de début n’est pas valide
            # r 99 la date de fin n’est pas valide
            # r 100 la date de fin est supérieure à la date de début
            # r 101 le numéro de mobile est bloqué et/ou blacklisté
            # r 102 le changement de Sender-ID vous oblige à rajouter «stop
            # SMS au 36001» à la fin de votre message



    # ---------
    #print("send_sms() ; from:",num," ; content:",sms[0:5],"(...)")
    return True

# ----------------------------------------------------------------------------
def sirene_send_email(subject,text_content, from_email, clean_email):
    try:
        msg = mail.EmailMultiAlternatives(subject, text_content, from_email, [clean_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except:
        return False

# ----------------------------------------------------------------------------
def sirene_get_notification(ninf):
    """ compute list of sms and emails for an event"""
    emails={}
    sms={}

    for grp in ninf.notify_groups.all():
        for contact in grp.contacts.all():
            if contact.is_active:
                if contact.want_email:
                    emails[contact.email]=1
                if contact.want_sms:
                    sms[contact.mobile]=1

    return (emails,sms)

# ----------------------------------------------------------------------------
def sirene_send_notification(ninf):
    """Send all notifications for event"""

    result = True
    (emails, sms) = sirene_get_notification(ninf)

    # emails
    # ------
    if ninf.visible and ninf.send_email and not ninf.is_template:
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
            print("Mail failed : ",dest)
            result=False

    # SMS
    # ---
    if ninf.visible and ninf.send_sms and not ninf.is_template:
        sms_content = render_to_string('app_sirene/sms.txt', {'info': ninf})
        for dest in sms.keys():
            if not sirene_send_sms(dest,sms_content):
                result = False
    return result

