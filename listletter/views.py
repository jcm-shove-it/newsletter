# Create your views here.
from django.http import HttpResponse


from django.contrib.auth.decorators import permission_required, login_required
from django.template import RequestContext, Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import PermissionDenied


from listletter.models import EmailTarget
from listletter.models import EmailTargetGroup
from listletter.models import ListletterSender

def main(request):
    return redirect('/listletter', permanent=True)

def index(request):
    return render_to_response(
        'listletter/index.html', 
        { 
            'isHome':True
        }
    )
        
@permission_required('listletter.can_send')
def addressindex(request):

    userName=request.user.username
    email_target_list = EmailTarget.objects.filter(user__user__username=userName)

    return render_to_response(
        'listletter/addressindex.html',
        {
            'email_target_list': email_target_list,
            'isContacts':True,
            'sidebar':True
        }
    )
        
@permission_required('listletter.can_send')
def groupindex(request):
    all_groups = EmailTargetGroup.objects.filter(user__user__username=request.user.username)
    return render_to_response(
        'listletter/groupindex.html', 
        {
            'all_groups': all_groups,
            'isContacts':True,
            'sidebar':True,
        }
    )
    
@permission_required('listletter.can_send')
def addressdetail(request, contact_id):

    mode = 'initial'
    email = None
    emailTargetId = None

    #############
    # find mode #
    #############
    try:
        emailTargetId = request.POST['id']
    except Exception as e:
        # no post data
        mode = 'display'
        emailTargetId = contact_id

    if mode != 'display':
        if emailTargetId == 'None':
            try:
                if request.POST['_save_goto_contacts'] != None:
                    mode = 'create__goto_contacts'
            except Exception as e:
                mode = 'create'
            emailTargetId = 0
        else:
            try:
                if request.POST['_save_goto_contacts'] != None:
                    mode = 'change__goto_contacts'
            except Exception as e:
                mode = 'change'


    #######################################
    # check if user is allowed to display #
    #######################################
    if int(emailTargetId) != 0:
        if EmailTarget.objects.get(id=emailTargetId).user.user.username != request.user.username:
            raise PermissionDenied

    ###################
    # execute request #
    ###################
    if mode == 'display':
        try:
            email = EmailTarget.objects.get(id=int(emailTargetId))
        except EmailTarget.DoesNotExist as e:
            email = EmailTarget()
    elif mode.startswith('create') or mode.startswith('change'):
        if mode.startswith('create'):
            email = EmailTarget()
        elif mode.startswith('change'):
            email = EmailTarget.objects.get(id=emailTargetId)
        email.name = request.POST['name']
        email.address = request.POST['address']
        email.user = ListletterSender.objects.filter(user__username=request.user.username)[0]
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
            'isContacts':True,
             'sidebar':True,
            })
    else:
        return render_to_response('listletter/addressdetail.html', {
            'email': email,
            'groups': EmailTargetGroup.objects.filter(user__user__username=request.user.username),
            'isContacts':True,
             'mode': mode
            })

@permission_required('listletter.can_send')
def groupdetail(request, group_id):
    mode = 'initial'
    group = None
    emailTargetGroupId = None

    #############
    # find mode #
    #############
    try:
        emailTargetGroupId = request.POST['id']
    except Exception as e:
        # no post data
        mode = 'display'
        emailTargetGroupId = group_id

    if mode != 'display':
        if emailTargetGroupId == 'None':
            try:
                if request.POST['_save_goto_groups'] != None:
                    mode = 'create_goto_groups'
            except Exception as e:
                mode = 'create'
            emailTargetGroupId = 0
        else:
            try:
                if request.POST['_save_goto_groups'] != None:
                    mode = 'change_goto_groups'
            except Exception as e:
                mode = 'change'
    

    #######################################
    # check if user is allowed to display #
    #######################################
    if int(emailTargetGroupId) != 0:
        if EmailTargetGroup.objects.get(id=emailTargetGroupId).user.user.username != request.user.username:
            raise PermissionDenied

    ###################
    # execute request #
    ###################
    if mode == 'display':
        try:
            group = EmailTargetGroup.objects.get(id=emailTargetGroupId)
        except EmailTargetGroup.DoesNotExist as e:
            group = EmailTargetGroup()
    elif mode.startswith('create') or mode.startswith('change'):
        if mode.startswith('create'):
            group = EmailTargetGroup()
        elif mode.startswith('change'):
            group = EmailTargetGroup.objects.get(id=emailTargetGroupId)
        group.name = request.POST['name']
        group.description = request.POST['description']
        group.user = ListletterSender.objects.filter(user__username=request.user.username)[0]
        group.save()

    if mode.endswith('goto_groups'):
        return render_to_response('listletter/groupindex.html', {
            'all_groups': EmailTargetGroup.objects.filter(user__user__username=request.user.username),
            'isContacts':True,
             'sidebar':True,
            })
    else:
        return render_to_response('listletter/addressgroupdetail.html', {
            'isContacts':True,
            'group': group,
            })

@permission_required('listletter.can_send')
def deleteaddress(request, contact_id):
    email = EmailTarget.objects.get(id=contact_id)
    email_name = email.name
    
    ######################################
    # check if user is allowed to delete #
    ######################################
    if email.user.user.username != request.user.username:
        raise PermissionDenied

    try:
        if request.POST['post'] == 'yes':
            email.delete()
            return render_to_response('listletter/deleteaddress.html', {
                'email':None,
                'email_name':email.name,
                'email_deleted': 'True',
                'isContacts':True
                })
    except:
        pass
    
    return render_to_response('listletter/deleteaddress.html', {
        'email': email,
        'email_name':email.name,
        'email_deleted': 'False',
        'isContacts':True
        })
           
@permission_required('listletter.can_send')
def deletegroup(request, group_id):
    group = EmailTargetGroup.objects.get(id=group_id)
    group_name = group.name
    
    ######################################
    # check if user is allowed to delete #
    ######################################
    if group.user.user.username != request.user.username:
        raise PermissionDenied

    try:
        if request.POST['post'] == 'yes':
            group.delete()
            return render_to_response('listletter/deleteaddressgroup.html', {
                'group':None,
                'group_name':group.name,
                'group_deleted': 'True',
                'isContacts':isContacts,
                })
    except:
        pass
    
    return render_to_response('listletter/deleteaddressgroup.html', {
        'group': group,
        'group_name':group.name,
        'group_deleted': 'False',
        'isContacts':True
        })

