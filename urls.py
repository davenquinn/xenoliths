from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView
from jsonrpc import jsonrpc_site
import samples.views

urlpatterns = patterns('',
    url(r'^json/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"), # for the graphical browser/web console only, omissible
    url(r'^json/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    #url(r'^json/(?P<method>[a-zA-Z0-9.]+)$', jsonrpc_site.dispatch), # for HTTP GET only, also omissible
    url(r'^data.json', 'samples.views.data'), # for HTTP GET only, also omissible

    # Examples:
    #url(r'^table/(?P<type>[\w]+)/', 'samples.views.table'),
    #url(r'^map/(?P<sample>[-\w\d]+)/', 'samples.views.map'),
    #url(r'^plot/(?P<type>[\w]+)/(?P<axes>[-\w\d]+)/', 'samples.views.plot'),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #    'document_root': settings.MEDIA_ROOT,
    #}),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
)

urlpatterns += staticfiles_urlpatterns()
