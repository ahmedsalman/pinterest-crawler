from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

import urllib2

from BeautifulSoup import BeautifulSoup

from scraper.pinterest.forms import URLForm


def scrap(request):


    desciption_list = []

    like_list = []
    like = ""
    
    comment_list = []
    comment = ""
    
    repin_list = []
    repin = ""

    if request.method == 'POST': # If the form has been submitted...
        form = URLForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            url = form.cleaned_data['url']
            source = BeautifulSoup(urllib2.urlopen(url).read())

            #extracting description
            for row in source('p', {'class' : 'description'}):
                desciption_list.append( row.string )


            for row in source('p', {'class' : 'stats colorless'}):
            
                #extracting number of likes
                if len( row.findAll('span')[0].string ) == 1:
                    like = "0 like"
                    like_list.append( like )
                else:
                    like = row.findAll('span')[0].string
                    like_list.append( like.strip() )

                #extracting number of comments
                if len( row.findAll('span')[1].string ) == 1:
                    comment = "0 comment"
                    comment_list.append( comment )
                else:
                    comment = row.findAll('span')[1].string
                    comment_list.append( comment.strip() )

                #extracting number of repins
                try:
                    if len( row.findAll('span')[2].string ) == 1:
                        repin = "0 repin"
                        repin_list.append( repin )
                except IndexError:
                        repin = "0 repin"
                        repin_list.append( repin )
                else:
                    repin = row.findAll('span')[2].string
                    repin_list.append( repin.strip() )


    final_result = [{"desciption_list": d, "like_list": l, "comment_list": c, "repin_list": r} for d, l, c, r in zip(desciption_list, like_list, comment_list, repin_list)]                    
    form = URLForm() # An unbound form
    
    data = {
        'form' : form,
        'final_result' : final_result,
        }
    template = "home.html"
    return render_to_response( template, data, 
                               context_instance = RequestContext( request ) )
