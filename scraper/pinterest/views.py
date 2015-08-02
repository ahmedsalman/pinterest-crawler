import re

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from BeautifulSoup import BeautifulSoup, NavigableString

from scraper.pinterest.forms import URLForm

invalid_tags = ['b', 'i', 'u']

def scrap(request):

    content_list = []
    form = URLForm() # An unbound form

    if request.method == 'POST': # If the form has been submitted...
        form = URLForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            url = form.cleaned_data['url']
            req = Request(url)
            try:
                response = urlopen(req)
                source = BeautifulSoup(urllib2.urlopen(url).read())
            except HTTPError, e:
                template = "404.html"
                return render_to_response( template, context_instance = RequestContext( request ) )
            except URLError, e:
                template = "500.html"
                return render_to_response( template, context_instance = RequestContext( request ) )
            else:
                source = BeautifulSoup(urllib2.urlopen(url).read())


            #Read the item block
            count = 0
            for row in source('div', {'class' : 'pinMeta '}):
                temp = {}
                try:
                    temp['description'] = row.find('p').text
                except AttributeError:
                    temp['description'] = "No description"
                try:
                    temp['repincount'] = source('em', {'class' : 'socialMetaCount repinCountSmall'})[count].text
                except:
                    temp['repincount'] = 0

                try:
                    temp['pinlink'] = source('em', {'class' : 'socialMetaCount likeCountSmall'})[count].text
                except:
                    temp['pinlink'] = 0

                try:
                    temp['pincomment'] = source('em', {'class' : 'socialMetaCount commentCountSmall'})[count].text
                except:
                    temp['pincomment'] = 0

                try:
                    temp['pinnedfrom'] = source('div', {'class' : 'creditTitle'})[count].text
                except:
                    temp['pinnedfrom'] = 0

                count = count+1
                content_list.append(temp)


    
    data = {
        'form' : form,
        'board_detail' : content_list,        
        }
    template = "home.html"
    return render_to_response( template, data, 
                               context_instance = RequestContext( request ) )
