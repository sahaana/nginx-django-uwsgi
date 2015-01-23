from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mysite.views.index', name='index'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
    url(r'^post/(?P<post_id>\d+)/detail.html$', 'mysite.views.post_detail', name='post_detail'),
    url(r'^post/form_upload.html$','mysite.views.post_form_upload', name='post_form_upload'),
    url(r'^list/$','mysite.views.list',name='list'),
    url(r'^spit/$','mysite.views.spit',name='spit'),
) + patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}))
