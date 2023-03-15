from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from .serializers import *

"""
POST http://127.0.0.1:8000/api/chat/message/ - add a new record
"""


@api_view(['POST'])
def send_message(request):
    if request.method == 'POST':
        try:
            serializers = AjaxChatSerializer(request.data)
            userInstance = AppUser.objects.get(pk=serializers.data['user'])
            roomInstance = Rooms.objects.get(pk=serializers.data['room'])
            current_chat = Chats()
            current_chat.user = userInstance
            current_chat.room = roomInstance
            current_chat.message = serializers.data['message']
            result = current_chat.save()
            return Response(result, status=status.HTTP_201_CREATED, template_name=None, content_type=None)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST, template_name=None, content_type=None)


"""
POST http://127.0.0.1:8000/api/login/ - authenticate record
"""


@api_view(['POST'])
def user_login(request):
    login_serializer = UserSerializer(request.data)

    user = authenticate(username=login_serializer.data['username'], password=login_serializer.data['password'])

    if user is not None:
        if user.is_active:
            result = login(request, user)
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        else:
            messages = 'Your account is disabled.'
            failed = True
            return Response(messages, status=status.HTTP_401_UNAUTHORIZED, template_name=None, content_type=None)

    else:
        messages = 'Invalid login details supplied.'
        failed = True
        return Response(messages, status=status.HTTP_400_BAD_REQUEST, template_name=None, content_type=None)


"""
POST http://127.0.0.1:8000/api/signup/ - add a new record
"""


@api_view(['POST'])
def signup(request):
    app_user_serializer = AppUserSerializer(request.data)
    user_instance = User.objects.create(app_user_serializer.data['user']).save()
    app_user_instance = AppUser.objects.create(
        user=user_instance,
        dob=app_user_serializer.data['dob'],
        gender=app_user_serializer.data['gender'],
    )
    try:
        result = app_user_instance.save()
        return Response(result, status=status.HTTP_201_CREATED, template_name=None, content_type=None)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR, template_name=None, content_type=None)


"""
GET http://127.0.0.1:8000/api/user/id - get user profile 
"""


@api_view(['GET'])
def get_profile(request, pk):
    try:
        current_user = AppUser.objects.get(user=User.objects.get(pk=pk))
        return Response(data=current_user, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_204_NO_CONTENT, template_name=None, content_type=None)


"""
GET http://127.0.0.1:8000/api/user/friends/id - get friends 
"""


@api_view(['GET'])
def get_all_friends(request, pk):
    try:
        current_user = AppUser.objects.get(user=User.objects.get(pk=pk))
        friends = current_user.friend.all()
        return Response(data=friends, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_204_NO_CONTENT, template_name=None, content_type=None)


"""
GET http://127.0.0.1:8000/api/user/room/id - get rooms 
"""


@api_view(['GET'])
def get_chat_rooms(request, pk):
    try:
        current_user = AppUser.objects.get(user=User.objects.get(pk=pk))
        rooms = current_user.rooms_set.all()
        return Response(data=rooms, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_204_NO_CONTENT, template_name=None, content_type=None)


"""
POST http://127.0.0.1:8000/api/friend/id - create friends
"""


@api_view(['POST'])
def add_friend(request, pk):
    try:
        current_user = AppUser.objects.get(user=User.objects.get(pk=pk))
        friend = AppUserSerializer(request.data)
        result = current_user.friend.add(friend)
        return Response(data=result, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_204_NO_CONTENT, template_name=None, content_type=None)


"""
POST http://127.0.0.1:8000/api/room/id - create room 
"""


@api_view(['POST'])
def add_room(request, pk):
    try:
        room_data = RoomSerializer(request.data)
        current_user = AppUser.objects.get(user=User.objects.get(pk=pk))
        room = Rooms.objects.create(
            name=room_data.data['name'],
            description=room_data.data['name'],
            user=current_user
        )
        result = room.save()
        return Response(data=result, status=status.HTTP_204_NO_CONTENT, content_type=None, template_name=None)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_204_NO_CONTENT, content_type=None, template_name=None)


"""
GET http://127.0.0.1:8000/api/chat/user_id/room_id - get chat history for a particular room 
"""


@api_view(['GET'])
def get_chat_history(request, user_id, room_id):
    try:
        current_user = AppUser.objects.get(user=User.objects.get(pk=user_id))
        current_room = Rooms.objects.get(pk=room_id)
        chats = Chats.objects.filter(user=current_user, room=current_room).values()

        return Response(data=chats, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_204_NO_CONTENT, template_name=None, content_type=None)