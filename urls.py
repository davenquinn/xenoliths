from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

#admin.autodiscover()

#import object_tools
#object_tools.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^table/(?P<type>[\w]+)/', 'samples.views.table'),
    #url(r'^plot/(?P<type>[\w]+)/', 'samples.views.plot'),
    url(r'^map/(?P<sample>[-\w\d]+)/', 'samples.views.map'),

    url(r'^plot/(?P<type>[\w]+)/(?P<axes>[-\w\d]+)/', 'samples.views.plot'),
	#url(r'^sample/(?P<sample>[-\w\d]+)/table', "samples.views.table"),
	#url(r'^mineral/(?P<mineral>[\w\d]+)/table', "samples.views.table"),
	#url(r'^mineral/(?P<mineral>[\w\d]+)/sample/(?P<sample>[-\w\d]+)/table', "samples.views.table"),
	#url(r'^sample/(?P<sample>[-\w\d]+)/mineral/(?P<mineral>[\w\d]+)/table', "samples.views.table"),


    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

urlpatterns += staticfiles_urlpatterns()