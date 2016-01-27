from listletter.models import EmailTargetGroup
from listletter.models import EmailTarget
import re

class Helper():
    # String to identify Mail address entrys in vcards
    MAIL_INIT_STRING = r'EMAIL'
    # String to identify Name entrys in vcards
    NAME_INIT_STRING = r'N:'
    # groups
    GROUPS_INIT_STRING = r'CATEGORIES:'
    
    @classmethod
    def getGroups(self, request):
        selected_group_ids = request.POST.getlist('groups')
        groups = []
        for group_id in selected_group_ids:
            group = EmailTargetGroup.objects.get(id=group_id)
            groups.append(group)

#        groups = []
#        for existing_group in EmailTargetGroup.objects.all():
#            try:
#                if str(request.POST[existing_group.name]) == 'on':
#                    groups.append(existing_group)
#            except Exception:
#                pass
        return groups

    @classmethod
    def importContacts(self, f):
        mail_re = re.compile(r'^(item.*)?' + self.MAIL_INIT_STRING + r'(.*)$', re.MULTILINE)
        name_re = re.compile(r'^' + self.NAME_INIT_STRING + r'(.*)$', re.MULTILINE)
        group_re = re.compile(r'^' + self.GROUPS_INIT_STRING + r'(.*)$', re.MULTILINE)
                
        Helper.cleanContacts()
        m_all = EmailTargetGroup.objects.get(name='all')
        imported = 0
        failed = []
        
        buf = f.read()
        re_vcard = re.compile(r'BEGIN:VCARD.*?END:VCARD', re.DOTALL)
        vcards = re_vcard.findall(buf)
        for vcard in vcards:
            emails = []
            if mail_re.search(vcard) != None:
                for email_tmp in mail_re.findall(vcard):
                    email_tmp = email_tmp[1]
                    email = email_tmp[email_tmp.find(":")+1:len(email_tmp)].strip()
                    emails.append(email)
                if name_re.search(vcard) != None:
                    tmp_name = name_re.search(vcard).group(1).replace(';', ' ').strip()
                else:
                    tmp_name = ''
                add_groups = []
                if group_re.search(vcard) != None:
                    groups_strs = group_re.search(vcard).group(1).replace(',', ' ').split()
                    for group_str in groups_strs:
                        add_group, created = EmailTargetGroup.objects.get_or_create(name = group_str)
                        add_groups.append(add_group)
                user = EmailTarget(name = tmp_name, address = emails[0])
                user.save()
                user.groups.add(m_all)
                if len(add_groups) > 0:
                    for add_group in add_groups:
                        user.groups.add(add_group)
                user.save()
                imported += 1
            else:
                failed.append(vcard)
        return imported, failed


    @classmethod
    def cleanContacts(self):
        EmailTarget.objects.all().delete()
        EmailTargetGroup.objects.all().delete()
        m_all = EmailTargetGroup(name='all')
        m_all.save()
        
        
