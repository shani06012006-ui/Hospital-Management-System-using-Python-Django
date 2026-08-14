from .models import Notification


def notifications(request):
    """Make unread count + latest notifications available in every template."""
    latest = Notification.objects.all()[:8]
    unread_count = Notification.objects.filter(is_read=False).count()
    return {
        'nav_notifications': latest,
        'nav_unread_count': unread_count,
    }