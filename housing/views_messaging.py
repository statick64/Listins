from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count, Max
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import CustomUser, Accommodation, Message

@login_required
def messaging_hub(request):
    """
    View for the main messaging hub where users can see their conversations
    and send/receive messages.
    """
    user = request.user
    
    # Get all conversations where the user is either sender or recipient
    conversations = CustomUser.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct()
    
    # Get the latest message for each conversation
    conversation_data = []
    for contact in conversations:
        latest_message = Message.objects.filter(
            (Q(sender=user) & Q(recipient=contact)) | 
            (Q(sender=contact) & Q(recipient=user))
        ).order_by('-timestamp').first()
        
        if latest_message:
            # Get unread count for this conversation
            unread_count = Message.objects.filter(
                sender=contact, 
                recipient=user,
                is_read=False
            ).count()
            
            # Get related accommodation if any
            accommodation = latest_message.accommodation
            
            conversation_data.append({
                'contact': contact,
                'latest_message': latest_message,
                'unread_count': unread_count,
                'accommodation': accommodation
            })
    
    # Sort conversations by latest message timestamp
    conversation_data = sorted(
        conversation_data, 
        key=lambda x: x['latest_message'].timestamp,
        reverse=True
    )
    
    # Check if a conversation is selected
    contact_id = request.GET.get('contact_id')
    selected_contact = None
    messages = []
    related_accommodation = None
    
    if contact_id:
        selected_contact = get_object_or_404(CustomUser, id=contact_id)
        messages = Message.objects.filter(
            (Q(sender=user) & Q(recipient=selected_contact)) | 
            (Q(sender=selected_contact) & Q(recipient=user))
        ).order_by('timestamp')
        
        # Mark messages as read
        Message.objects.filter(sender=selected_contact, recipient=user, is_read=False).update(is_read=True)
        
        # Get the most recent accommodation discussed, if any
        related_message = messages.filter(accommodation__isnull=False).order_by('-timestamp').first()
        if related_message:
            related_accommodation = related_message.accommodation
    
    # Get total unread messages count for the notification badge
    unread_messages_count = Message.objects.filter(recipient=user, is_read=False).count()
    
    context = {
        'conversations': conversation_data,
        'selected_contact': selected_contact,
        'messages': messages,
        'related_accommodation': related_accommodation,
        'unread_messages_count': unread_messages_count
    }
    
    return render(request, 'notifications/LandlordStudentMessagingHub.html', context)

@login_required
def send_message(request):
    """
    API view to send a new message
    """
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        content = request.POST.get('content')
        accommodation_id = request.POST.get('accommodation_id')
        
        recipient = get_object_or_404(CustomUser, id=recipient_id)
        
        # Create new message
        message = Message(
            sender=request.user,
            recipient=recipient,
            content=content
        )
        
        # Attach accommodation if provided
        if accommodation_id:
            accommodation = get_object_or_404(Accommodation, accommodation_id=accommodation_id)
            message.accommodation = accommodation
        
        message.save()
        
        return JsonResponse({
            'status': 'success',
            'message_id': message.id,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M'),
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def get_unread_messages_count(request):
    """
    API view to get the number of unread messages for the current user
    """
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})

@login_required
def start_conversation(request, property_id=None):
    """
    Start a conversation with a landlord about a specific property
    """
    if property_id:
        property = get_object_or_404(Accommodation, accommodation_id=property_id)
        landlord = property.landlord
        
        # Only students can initiate conversations about properties
        if request.user.user_type == 'Student' and landlord.user_type == 'Landlord':
            return redirect(f'/housing/messages/?contact_id={landlord.id}&property_id={property_id}')
    
    return redirect('housing:messaging_hub')
