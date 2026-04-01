from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import CustomUser
from profiles.models import Match  # 🔥 IMPORTANT
from .models import Message
from .serializers import MessageSerializer


# ---------------------
# Send message
# ---------------------
@api_view(['POST'])
def send_message(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')
    message = request.data.get('message')

    # Validate input
    if not sender_id or not receiver_id or not message:
        return Response({"error": "All fields are required"}, status=400)

    try:
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    # 🔥 CHECK IF USERS ARE MATCHED
    is_match = Match.objects.filter(user1=sender, user2=receiver).exists() or \
               Match.objects.filter(user1=receiver, user2=sender).exists()

    if not is_match:
        return Response({"error": "You can only chat with matched users"}, status=403)

    # Create message
    msg = Message.objects.create(
        sender=sender,
        receiver=receiver,
        message=message
    )

    return Response({
        "message": "Message sent successfully",
        "data": MessageSerializer(msg).data
    })


# ---------------------
# Get messages
# ---------------------
@api_view(['GET'])
def get_messages(request, user1_id, user2_id):

    # 🔥 CHECK IF USERS ARE MATCHED
    is_match = Match.objects.filter(user1_id=user1_id, user2_id=user2_id).exists() or \
               Match.objects.filter(user1_id=user2_id, user2_id=user1_id).exists()

    if not is_match:
        return Response({"error": "No conversation. Users are not matched"}, status=403)

    messages = Message.objects.filter(
        sender_id__in=[user1_id, user2_id],
        receiver_id__in=[user1_id, user2_id]
    ).order_by('timestamp')

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)