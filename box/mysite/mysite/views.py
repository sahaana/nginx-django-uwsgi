from mysite.forms import PostForm
from django.shortcuts import render
from mysite import models as m
from django.http import HttpResponseRedirect, HttpResponse, Http404 
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import redirect
 

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
