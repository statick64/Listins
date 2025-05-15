from .models import Message
from django.db.models import Q

def unread_messages_count(request):
    """
    Context processor that adds unread_messages_count to all templates.
    """
    count = 0
    if request.user.is_authenticated:
        count = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
    
    return {
        'unread_messages_count': count
    }
