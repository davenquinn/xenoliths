from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import RedirectView
from jsonrpc import jsonrpc_site
import .views

urlpatterns = patterns('',
    url(r'^json/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"), # for the graphical browser/web console only, omissible
    url(r'^json/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    #url(r'^json/(?P<method>[a-zA-Z0-9.]+)$', jsonrpc_site.dispatch), # for HTTP GET only, also omissible
    url(r'^data.json', 'views.data'), # for HTTP GET only, also omissible
    url(r'^$', RedirectView.as_view(url="/static/index.html")),
)

urlpatterns += staticfiles_urlpatterns()
