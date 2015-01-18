#models.py

from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db import models as m
                                                                                          
class Post(m.Model):                                                                      
    content = m.CharField(max_length=256)                                                 
    created_at = m.DateTimeField('Datetime created')                                      
                                                                                          
                                                                                          
def post_upload(request):
    if request.method == 'GET':
        return render(request, 'post/upload.html', {})
    elif request.method == 'POST':
        post = m.Post.objects.create(content=request.POST['content'],
                                     created_at=datetime.utcnow())
        # No need to call post.save() at this point -- it's already saved.
        return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))
    
