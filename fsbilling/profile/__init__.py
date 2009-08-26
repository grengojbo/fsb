# -*- mode: python; coding: utf-8; -*-
from django.contrib.auth.models import User
from userprofile import signals
from satchmo_store.contact.models import AddressBook, PhoneNumber, Contact, ContactRole
from l10n.models import Country
import logging
l = logging.getLogger('fsbilling.profile')

def handler_create_profile(sender, user, **kwargs):
    try:
        contact = Contact.objects.get(user=user)
    except Contact.DoesNotExist:
        contact = Contact()
    
    contact.user = user
    #contact.first_name = first_name
    #contact.last_name = last_name
    contact.email = user.email
    contact.role = ContactRole.objects.get(pk='Customer')
    contact.title = ''
    contact.save()
    l.debug("Signal Profile Create default -> satchmo_registration_verified")
    signals.satchmo_registration_verified.send(sender=sender, contact=contact)
    
signals.profile_registration.connect(handler_create_profile)