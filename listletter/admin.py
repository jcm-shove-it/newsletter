from listletter.models import ListletterSender
from listletter.models import EmailTargetGroup
from listletter.models import EmailTarget
from listletter.models import SendListletterAction
from listletter.models import SendAction
from listletter.models import SendError

from django.contrib import admin


admin.site.register(ListletterSender)
admin.site.register(EmailTargetGroup)
admin.site.register(EmailTarget)
admin.site.register(SendListletterAction)
admin.site.register(SendAction)
admin.site.register(SendError)



