from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newsletter.views.home', name='home'),
    # url(r'^newsletter/', include('newsletter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    url(r'^listletter/$', 'newsletter.listletter.views.index'),
    url(r'^listletter/addressindex/$$', 'newsletter.listletter.views.addressindex'),
    #url(r'^listletter/groupindex/$$', 'newsletter.listletter.views.groupindex'),                   
    #url(r'^listletter/mailindex/$', 'newsletter.listletter.views.mailindex'),
    #url(r'^listletter/approve/$', 'newsletter.listletter.views.approve'),
    #url(r'^listletter/sendmail/$', 'newsletter.listletter.views.sendmail'),
    #url(r'^listletter/selectmail/$', 'newsletter.listletter.views.selectmail'),
    #url(r'^listletter/groupindex/(?P<group_id>\d+)/$', 'newsletter.listletter.views.groupdetail'),
    #(r'^listletter/groupindex/(?P<group_id>\d+)/delete/$', 'newsletter.listletter.views.deletegroup'),
    url(r'^listletter/addressindex/(?P<contact_id>\d+)/$', 'newsletter.listletter.views.addressdetail'),
    #url(r'^listletter/addressindex/(?P<contact_id>\d+)/delete/', 'newsletter.listletter.views.deleteaddress'),
    #url(r'^listletter/send/(?P<email_id>\d+)/', 'newsletter.listletter.views.sendmail'),
    #url(r'^listletter/contactupload/', 'newsletter.listletter.views.upload_contacts'),
    #url(r'^listletter/deletemailindex/$$', 'newsletter.listletter.views.deletemailindex'),
    #url(r'^listletter/deletemailindex/(?P<email_id>\d+)/$', 'newsletter.listletter.views.deletemail'),
    #url(r'^listletter/sentmailhistory/$$', 'newsletter.listletter.views.sentmailhistory'),
    #only in development engine !
    #url(r'^listletter/site_media/(?P<path>.*)$', 'django.views.static.serve',
    # {'document_root': '/home/jcm/repos/django/newsletter/htdocs/site_media/'}),

                       
)
