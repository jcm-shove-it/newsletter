# Create your views here.
from django.http import HttpResponse


from django.contrib.auth.decorators import permission_required, login_required
from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

from listletter.models import EmailTarget
from listletter.models import EmailTargetGroup
from listletter.models import ListletterSender


def index(request):
    a=[]
    isHome=True
    for i in range(1000):
        a.append(i)
    t = loader.get_template('listletter/index.html')
    c = Context({'cnt':a, 'isHome':isHome})
    return HttpResponse(t.render(c))

@permission_required('listletter.can_send')
def addressindex(request):

    isContacts=True
    userName=request.user.username

    email_target_list = EmailTarget.objects.filter(user__user__username=userName)
    t = loader.get_template('listletter/addressindex.html')
    c = Context(
        {
            'email_target_list': email_target_list,
            'isContacts':isContacts,
            'sidebar':True,
        }
        )
    return HttpResponse(t.render(c))


@permission_required('listletter.can_send')
def addressdetail(request, contact_id):
    isContacts=True
    mode = ''
    email = None

    try:
        if request.POST['id'] == 'None':
            try:
                if request.POST['_save_goto_contacts'] != None:
                    mode = 'create__goto_contacts'
            except Exception as e:
                mode = 'create'
        else:
            try:
                if request.POST['_save_goto_contacts'] != None:
                    mode = 'change_goto_contacts'
            except Exception as e:
                mode = 'change'
                
    except Exception as e:
        # no post data
        mode = 'display'

    if mode == 'display':
        try:
            email = EmailTarget.objects.get(id=int(contact_id),user__user__username=request.user.username)
        except EmailTarget.DoesNotExist as e:
            email = EmailTarget()
    elif mode.startswith('create') or mode.startswith('change'):
        if mode.startswith('create'):
            email = EmailTarget()
        elif mode.startswith('change'):
            email = EmailTarget.objects.get(id=request.POST['id'],user__user__username=request.user.username)
        email.name = request.POST['name']
        email.address = request.POST['address']
        userName = request.user.username
        llSender = ListletterSender.objects.filter(user__username=userName)
        email.user = llSender[0]
        #try:
        #    a = request.POST['active']
        #    if a == 'on':
        #        email.active = True
        #except:
        #    email.active = False
        email.save()
        liste = request.POST.getlist('groups')
        email.groups.clear()
        for group_id in liste:
            group = EmailTargetGroup.objects.get(id=group_id,user__user__username=request.user.username)
            email.groups.add(group)
        email.save()

    if mode.endswith('goto_contacts'):
        return render_to_response('listletter/addressindex.html', {
            'email_target_list': EmailTarget.objects.filter(user__user__username=request.user.username),
            'isContacts': True,
            'sidebar':True,
            })
    else:
        return render_to_response('listletter/addressdetail.html', {
            'email': email,
            'groups': EmailTargetGroup.objects.filter(user__user__username=request.user.username),
            'isContacts':isContacts
            })
