from django.db import models

# Create your models here.

from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.models import User
from email.parser import HeaderParser
from email.parser import Parser
from email import Header
from email.message import Message
from email.utils import parsedate
from email.utils import parseaddr
import time

class ListletterSender(models.Model):
    emailAddress = models.CharField('email address of sender for from entries', max_length=128)
    mailUsername = models.CharField('username on mail server for send actions', max_length=128)
    mailPassword = models.CharField('password on mail server for send actions', max_length=128)
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        )
    def __unicode__(self):
        return self.user.username
    def allowedForEmailTarget(self, emailTarget):
        if type(emailTarget) == EmailTarget:
            if not emailTarget.user == self:
                raise InvalidEmailTarget4User("EmailTarget %s does not belong to ListletterSender %s" % (str(emailTarget.id), self.__unicode__()))
        else:
            InvalidEmailTarget4User("emailTarget %s is not of type EmailTarget" % str(emailTarget))
        
    
class EmailTargetGroup(models.Model):
    def __unicode__(self):
        return self.name
    name        = models.CharField('group name', max_length=30)
    description = models.CharField('group description', max_length=1024)
    user        = models.ForeignKey(ListletterSender)

class EmailTarget(models.Model):
    def __unicode__(self):
        return self.address

    name    = models.CharField(max_length=128)
    address = models.CharField('email address', max_length=320)
    active  = models.BooleanField('non-active addresses will recieve no emails', default=True)
    created = models.DateTimeField('date created', default=datetime.now)
    user    = models.ForeignKey(ListletterSender)
    groups  = models.ManyToManyField(EmailTargetGroup, blank=True)

class SendListletterAction(models.Model):
    STATI = (
        (u'ST', u'started'),
        (u'FI', u'finished'),
        )
    date_start = models.DateTimeField('start sending the serial letter', null=True)
    date_end   = models.DateTimeField('end sending the serial letter', null=True)
    sender_address = models.CharField(max_length=320)
    user       = models.ForeignKey(ListletterSender)
    status     = models.CharField(max_length=2, choices = STATI)

class SendAction(models.Model):
    def __unicode__(self):
        return self.sendlistletter.user + ' ' + str(self.date)
    date      = models.DateTimeField('send date', default=datetime.now)
    recipient = models.CharField('email address', max_length=320)
    sendlistletter = models.ForeignKey(SendListletterAction)
    class Meta:
        permissions = (
            ("can_send", "Can send list emails"),
            )

class SendError(models.Model):
    def __unicode__(self):
        return self.error_str + str(self.date)
    date      = models.DateTimeField('send date', default=datetime.now)
    recipient = models.CharField(max_length=320)
    error_str = models.CharField(max_length=1000)
    sendlistletter = models.ForeignKey(SendListletterAction)
   
#temporary container for all mails to be selected or sent
class Email(models.Model):
    def __unicode__(self):
        return self.uid
    header  = models.TextField(max_length=100000)
    uid     = models.IntegerField()

    def getSubject(self):
        email_hdr = HeaderParser().parsestr(self.header, True)
        subject = email_hdr.get('SUBJECT')
        return subject

    def getMultipart(self):
        return HeaderParser.parsestr(self.header, True).is_multipart()

    def getCharset(self):
        return HeaderParser.parsestr(self.header, True).get_payload().get_charset().get_body_encoding()

    def getDate(self):
        email_hdr = HeaderParser().parsestr(self.header, True)
        date = email_hdr.get('DATE')
        date_parsed = parsedate(date)
        return time.strftime('%d.%m.%Y', time.localtime(time.mktime(date_parsed)))

    def getSender(self):
        email_hdr = HeaderParser().parsestr(self.header, True)
        return parseaddr(email_hdr.get('FROM'))[1]


