from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, read=False)
        return {'unread_notifications': unread_notifications}
    return {}