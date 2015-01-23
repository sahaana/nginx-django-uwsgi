import sys
sys.path.insert(0, '/Users/meep_me/Desktop/ram_stuff/combining/box/mysite/protobuff_files')


from mysite.forms import PostForm, DocumentForm
from django.shortcuts import render, render_to_response
from mysite import models as m
from django.http import HttpResponseRedirect, HttpResponse, Http404 
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from mysite.settings import MEDIA_ROOT

import requests
from google.protobuf.text_format import Merge
import realtime_bidding_pb2 as rtb
import binascii
 

def index(request):
    return redirect('media/media.png')

def post_detail(request, post_id):
    try:
        post = m.Post.objects.get(pk=post_id)
    except m.Post.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404
    return render(request, 'post/detail.html', {'post': post})


def post_form_upload(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm
 
        if form.is_valid():
            content = form.cleaned_data['content']
            created_at = form.cleaned_data['created_at']
            post = m.Post.objects.create(content=content,created_at=created_at)
            return HttpResponseRedirect(reverse('post_detail',kwargs={'post_id': post.id}))
 
    return render(request, 'post/post_form_upload.html', {
        'form': form,
    })

def list(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES) #why taking in 2 things: .FILES is how data gets bound
        if form.is_valid():
            newdoc = m.Document(docfile = request.FILES['docfile'])
            #request.FILES['docfile'].read()
            newdoc.save()
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()
    documents = m.Document.objects.all()
    return render_to_response('post/list.html', {'documents':documents,'form':form}, context_instance=RequestContext(request))

def spit(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES) #why taking in 2 things: .FILES is how data gets bound
        if form.is_valid():
            newdoc = m.Document(docfile = request.FILES['docfile'])
            #request.FILES['docfile'].read()
            newdoc.save()
            return HttpResponseRedirect(reverse('spit'))
    else:
        form = DocumentForm()
    try:
        documents = m.Document.objects.all()[m.Document.objects.count()-1]
        f = open(MEDIA_ROOT+'/'+str(documents.docfile))
        bid = f.read()#.replace('\n', '<br/>')
        f.close()
        a = rtb.BidRequest()
        Merge(bid, a)
        payload = a.SerializeToString()
        url = "http://test.bidr.io/bid/adx"
        r = requests.post(url,payload)
        bid = r.content
        if r.ok:
            #can only handle 45 bytes at a time
            r = bin2a_uu(bid)
    except AssertionError:
        bid = "No Prior Bid Requests"
    return render_to_response('post/spit.html', {'documents':bid,'form':form}, context_instance=RequestContext(request))

