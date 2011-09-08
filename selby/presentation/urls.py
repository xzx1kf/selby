from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^matthew/$', 'matthew.views.list_courses'),
    (r'^matthew/(?P<course_id>\d+)/$', 'matthew.views.list_races'),
    (r'^matthew/\d+/(?P<race_id>\d+)/$', 'matthew.views.list_horses'),
    (r'^matthew/layem/$', 'matthew.views.layem'),

    # Examples:
    # url(r'^$', 'presentation.views.home', name='home'),
    # url(r'^presentation/', include('presentation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
