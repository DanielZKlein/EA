from django.conf.urls.defaults import *
from EA.game.views import game

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('EA.core',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
	(r'^$', 'views.rootview'),
	(r'^privatepage/$', 'views.private'),
	(r'^publicpage/$', 'views.public'),
	(r'^publicpagewithsecret/$', 'views.publicsecret'),
	(r'^login/$',  'views.loginpage'),
	(r'^dologin/$', 'views.dologin'),
	(r'^dologout/$', 'views.dologout'),
)

urlpatterns = urlpatterns + patterns('EA.game',
	(r'^prelobby/$', 'views.prelobby'),
	url(r'^game/(\d+)/$', 'views.game', name='gameview'),
)

urlpatterns = urlpatterns + patterns('',
	(r'^stuff/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'c:\code\EA\stuff'}),
)
