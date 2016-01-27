import imaplib
from email.parser import HeaderParser
from email.parser import Parser
from email import Header
from email.message import Message
from listletter.models import Email
import re

class InboxSupplier:
    M = None
    
    def __init__(self):
        pass


    def login(self, hostname, username, password):
        self.M = imaplib.IMAP4_SSL(hostname)
        self.M.login(username, password)


    def listMails(self):
        list = []
        code, cnt = self.M.select()
        for i in range(1, int(cnt[0])+1):
            uid = map(int, re.findall(r'\d+ \(UID (\d+)\)', self.M.fetch(i, '(UID)')[1][0]))[0]

            header_str = self.M.fetch(i, 'RFC822.HEADER')[1][0][1]
            header = HeaderParser().parsestr(header_str, True)
            subject = header.get('SUBJECT')
            m_mail = Email()
            m_mail.header = header_str
            m_mail.uid = uid
            list.append(m_mail)
        return(list)

    def logout(self):
        self.M.logout()
        self.M = None
        
    #should not be used
    #def getEmailMessage(self, uid):
    #    return 'error'
    #    code, cnt = self.M.select()
    #    typ, a = self.M.search(None, '(UID ' + str(uid) + ')')
    #    i = int(a[0])
    #    body_str = self.M.fetch(i, 'RFC822')[1][0][1]
    #    m_mail = Parser().parsestr(body_str)
    #    return m_mail
        
    def getEmail(self, uid):
        code, cnt = self.M.select()
        typ, a = self.M.search(None, '(UID ' + str(uid) + ')')
        i = int(a[0])
        body_str = self.M.fetch(i, 'RFC822')[1][0][1]
        header_str = self.M.fetch(i, 'RFC822.HEADER')[1][0][1]
        header = HeaderParser().parsestr(header_str, True)
        subject_str = header.get('SUBJECT')
        m_mail = Email()
        m_mail.header = header_str
        m_mail.uid = uid
        m_mail.body = body_str
        return m_mail

    def deleteMail(self, uid):
        code, cnt = self.M.select()
        typ, a = self.M.search(None, '(UID ' + str(uid) + ')')
        if len(a) == 1:
            self.M.store(a[0], 'FLAGS', '(\Deleted)')
            self.M.expunge()

