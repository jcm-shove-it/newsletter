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
    (r'^admin/', include(admin.site.urls)),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

    (r'^listletter/$', 'newsletter.listletter.views.index'),
    (r'^listletter/addressindex/$$', 'newsletter.listletter.views.addressindex'),
    (r'^listletter/groupindex/$$', 'newsletter.listletter.views.groupindex'),                   
    (r'^listletter/mailindex/$', 'newsletter.listletter.views.mailindex'),
    #(r'^listletter/approve/$', 'newsletter.listletter.views.approve'),
    (r'^listletter/sendmail/$', 'newsletter.listletter.views.sendmail'),
    #(r'^listletter/selectmail/$', 'newsletter.listletter.views.selectmail'),
    (r'^listletter/groupindex/(?P<group_id>\d+)/$', 'newsletter.listletter.views.groupdetail'),
    (r'^listletter/groupindex/(?P<group_id>\d+)/delete/$', 'newsletter.listletter.views.deletegroup'),
    (r'^listletter/addressindex/(?P<contact_id>\d+)/$', 'newsletter.listletter.views.addressdetail'),
    (r'^listletter/addressindex/(?P<contact_id>\d+)/delete/', 'newsletter.listletter.views.deleteaddress'),
    (r'^listletter/send/(?P<email_id>\d+)/', 'newsletter.listletter.views.sendmail'),
    (r'^listletter/contactupload/', 'newsletter.listletter.views.upload_contacts'),
    (r'^listletter/deletemailindex/$$', 'newsletter.listletter.views.deletemailindex'),
    (r'^listletter/deletemailindex/(?P<email_id>\d+)/$', 'newsletter.listletter.views.deletemail'),
    (r'^listletter/sentmailhistory/$$', 'newsletter.listletter.views.sentmailhistory'),
    #only in development engine !
    #(r'^listletter/site_media/(?P<path>.*)$', 'django.views.static.serve',
    # {'document_root': '/home/jcm/repos/django/newsletter/htdocs/site_media/'}),

                       
)
