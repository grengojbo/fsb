# -*- mode: python; coding: utf-8; -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from forms import PrepaidCodeForm, PrepaidStartForm
from livesettings import config_get_group
from django.shortcuts import redirect
import logging
from django.views.decorators.csrf import csrf_exempt
from models import PrepaidLog
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from fsa.directory.models import Endpoint
from django.contrib.auth import login
from django.contrib.auth import authenticate

log = logging.getLogger("fsb.prepaid.views")

gc = config_get_group('PAYMENT_PREPAID')

@login_required
def prepaid_form(request, template_name='prepaid/activate.html',
             success_url='profile_overview', extra_context=None, **kwargs):
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    if PrepaidLog.objects.is_valid(ipconnect=request.META['REMOTE_ADDR'], username=request.user):
        if request.method == "POST":
            form = PrepaidCodeForm(request, data=request.POST, files=request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                log.debug('form valid {0}'.format(data))
                return redirect(success_url)
        else:
            form = PrepaidCodeForm(request)

        return render_to_response(template_name, {'form': form, 'subsection': 'money', 'section': 'profile'}, context_instance=context)
    else:
        return render_to_response('prepaid/block.html', {'ip':request.META['REMOTE_ADDR']}, context_instance=context)

@csrf_exempt
def prepaid_start_form(request, template_name='prepaid/start.html',
             success_url='profile_overview', extra_context=None, **kwargs):
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    if PrepaidLog.objects.is_valid(ipconnect=request.META['REMOTE_ADDR']):
        if request.method == "POST":
            form = PrepaidStartForm(request, data=request.POST, files=request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                #log.debug('form valid {0}'.format(data))
                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(request)

                new_user = User.objects.get(username__iexact=data.get('username'))
                if data.get('email'):
                    new_user.email = data.get('email')
                if data.get('last_name'):
                    new_user.last_name = data.get('last_name')
                if data.get('first_name'):
                    new_user.first_name = data.get('first_name')
                new_user.save()
                #signals.user_activated.send(sender=self.__class__, user=new_user, request=request)
                endpoint = Endpoint.objects.get(uid__exact=data.get('prnumber'))
                endpoint.site = site
                endpoint.save()
                #endpoint_create.send(sender=self.__class__, endpoint=endpoint)
                # TODO: добавить отпраку почты с данными endpoint
                user = authenticate(username=data.get('username'), password=data.get('password1'))
                login(request, user)
                return redirect(success_url)
        else:
            form = PrepaidStartForm(request)

        return render_to_response(template_name, {'form':form}, context_instance=context)
    else:
        return render_to_response('prepaid/block.html', {'ip':request.META['REMOTE_ADDR']}, context_instance=context)

