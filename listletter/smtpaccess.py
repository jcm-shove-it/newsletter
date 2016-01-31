import smtplib
import email
import sys
import datetime
from listletter.models import SendError
from listletter.models import SendAction
from listletter.models import SendListletterAction

from django.core.exceptions import PermissionDenied

class SmtpSender:
    server = None

    def login(self, server, username, password):
        self.server = smtplib.SMTP(server)
        self.server.ehlo()
        self.server.login(username, password)
        
    def logout(self):
        self.server.quit()
        self.server = None


    def sendMail(self, m_email, email_target_list, llSender):

        if self.server == None:
            raise PermissionDenied

        # get SendListletterAction
        m_listletteraction = SendListletterAction()
        m_listletteraction.user = llSender
        m_listletteraction.subject = m_email.get('')

        # change Date header in mail
        m_key = 'Date'
        if m_email.get(m_key) != None:
            m_email.__delitem__(m_key)
        m_email.__setitem__(m_key, email.utils.formatdate())

        #change from in mail
        m_key = 'From'
        if m_email.get(m_key) != None:
            m_email.__delitem__(m_key)
        my_from = u'%s %s<%s>' % (llSender.firstName, llSender.lastName, llSender.emailAddress)
        my_hdr = email.header.Header(my_from, 'iso-8859-1')
        m_email.__setitem__(m_key, my_hdr)

        # set mail sender in m_listletteraction
        sender = ''
        m_key = 'From'
        if m_email.get(m_key) != None:
            sender = m_email.get(m_key)
            m_listletteraction.sender_address = sender

        # set mail seubject in m_listletteraction
        subject = ''
        m_key = 'Subject'
        if m_email.get(m_key) != None:
            subject = m_email.get(m_key)
            m_listletteraction.subject = subject

        err_cnt = 0
        suc_cnt = 0

        m_listletteraction.date_start = datetime.datetime.now()
        m_listletteraction.status = 'ST'
        m_listletteraction.save()

        for email_trg in email_target_list:
            if email_trg.active == False:
                continue

            # change message id
            m_key = 'Message-ID'
            if m_email.get(m_key) != None:
                m_email.__delitem__(m_key)
            m_email.__setitem__(m_key, email.utils.make_msgid('shove-it_listletter'))

            m_key = 'To'
            if m_email.get(m_key) != None:
                m_email.__delitem__(m_key)
            my_to  = u'%s<%s>' % (email_trg.name, email_trg.address)
            my_hdr = email.header.Header(my_to, 'iso-8859-1')
            m_email.__setitem__(m_key, my_hdr)
            
            try:
                self.server.sendmail(sender, email_trg.address, m_email.as_string())
                sA = SendAction()
                sA.recipient = email_trg.address
                sA.sendlistletter = m_listletteraction
                sA.save()
                suc_cnt += 1
                m_listletteraction.date_end = datetime.datetime.now()
                m_listletteraction.status = 'FI'
                m_listletteraction.save()
            except smtplib.SMTPRecipientsRefused:
                err_cnt += 1
                err = SendError()
                err.error_str = 'SMTPRecipientsRefused'
                err.recipient = email_trg.address 
                err.sendlistletter = m_listletteraction
                err.save()
                m_listletteraction.date_end = datetime.datetime.now()
                m_listletteraction.status = 'FI'
                m_listletteraction.save()
            except smtplib.SMTPDataError:
                err_cnt += 1
                err = SendError()
                err.error_str = 'SMTPDataError'
                err.recipient = email_trg.address 
                err.sendlistletter = m_listletteraction
                err.save()
                m_listletteraction.date_end = datetime.datetime.now()
                m_listletteraction.status = 'FI'
                m_listletteraction.save()
            except smtplib.SMTPConnectError:
                err_cnt += 1
                err = SendError()
                err.error_str = 'SMTPConnectError'
                err.recipient = email_trg.address 
                err.sendlistletter = m_listletteraction
                err.save()
                m_listletteraction.date_end = datetime.datetime.now()
                m_listletteraction.status = 'FI'
                m_listletteraction.save()
            except smtplib.SMTPHeloError:
                err_cnt += 1
                err = SendError()
                err.error_str = 'SMTPHeloError'
                err.recipient = email_trg.address 
                err.sendlistletter = m_listletteraction
                err.save()
                m_listletteraction.date_end = datetime.datetime.now()
                m_listletteraction.status = 'FI'
                m_listletteraction.save()
            except smtplib.SMTPAuthenticationError:
                err_cnt += 1
                err = SendError()
                err.error_str = 'SMTPAuthenticationError'
                err.recipient = email_trg.address 
                err.sendlistletter = m_listletteraction
                err.save()
                m_listletteraction.date_end = datetime.datetime.now()
                m_listletteraction.status = 'FI'
                m_listletteraction.save()
            except:
                err_cnt += 1
                err = SendError()
                err.error_str = str(sys.exc_info()[0])
                err.recipient = email_trg.address
                err.sendlistletter = m_listletteraction
                err.save()
                m_listletteraction.date_end = datetime.datetime.now()
                m_listletteraction.status = 'FI'
                m_listletteraction.save()

        return m_listletteraction
