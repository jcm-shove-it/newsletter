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

        return groups

    @classmethod
    def importContacts(self, f, llSender):
        mail_re = re.compile(r'^(item.*)?' + self.MAIL_INIT_STRING + r'(.*)$', re.MULTILINE)
        name_re = re.compile(r'^' + self.NAME_INIT_STRING + r'(.*)$', re.MULTILINE)
        group_re = re.compile(r'^' + self.GROUPS_INIT_STRING + r'(.*)$', re.MULTILINE)
                
        Helper.cleanContacts(llSender)
        m_all = EmailTargetGroup.objects.get(name='all', user = llSender)
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
                    groups_strs = group_re.search(vcard).group(1).split(',')
                    for group_str in groups_strs:
                        group_str = group_str.strip()
                        add_group, created = EmailTargetGroup.objects.get_or_create(name = group_str, user = llSender)
                        add_groups.append(add_group)
                user = EmailTarget(name = tmp_name, address = emails[0], user = llSender)
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
    def cleanContacts(self, llSender):
        EmailTarget.objects.filter(user=llSender).delete()
        EmailTargetGroup.objects.filter(user=llSender).delete()
        m_all = EmailTargetGroup(name='all', user=llSender)
        m_all.save()

    @classmethod
    def getUsersOfGroups(self, groups, llSender):
        selected_email_targets = []

        available_email_targets = EmailTarget.objects.filter(user__user__username=llSender.user.username)
        for available_email_target in available_email_targets:
            send_mail = False
            for group in groups:
                for user_group in available_email_target.groups.all():
                    if user_group.id == group.id:
                        send_mail = True
            if send_mail == True:
                selected_email_targets.append(available_email_target)
        return selected_email_targets

        
