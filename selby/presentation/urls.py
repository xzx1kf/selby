from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^matthew/$', 'matthew.views.index'),
    (r'^matthew/(?P<matthew_id>\d+)/$', 'matthew.views.detail'),
    # Examples:
    # url(r'^$', 'presentation.views.home', name='home'),
    # url(r'^presentation/', include('presentation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
