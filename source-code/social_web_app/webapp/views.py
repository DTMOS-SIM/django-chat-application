from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def user_login(request):
    errors = ""
    messages = ""
    failed = False;

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)

        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../home/')
            else:
                messages = 'Your account is disabled.'
                failed = True
        else:
            messages = 'Invalid login details supplied.'
            failed = True
    else:
        login_form = LoginForm()

    return render(request, './login.html', {
        'login_form': login_form,
        'errors': errors,
        'message': messages,
        'failed': failed
    })


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../login')


def signup(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(request.POST['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'dob' and 'gender' in user_form.cleaned_data:
                profile.dob = request.DATA['dob']
                profile.gender = request.DATA['gender']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, './sign-up.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered, })


def lost_password(request):
    return render(request, './lost-password.html')


"""
Home Page Endpoints
"""


@login_required(login_url='/login/')
def home(request):
    global current_user_id
    current_user_id = int(request.user.id)
    global current_user
    current_user = AppUser.objects.get(user=User.objects.get(pk=current_user_id))

    if request.method == 'POST' and request.FILES['description']:

        image_form_raw = ImageMediaForm(request.POST, request.FILES)

        if image_form_raw.is_valid():
            image_form_initial = image_form_raw.save(commit=False)

            upload = request.FILES['description']
            fss = FileSystemStorage()

            file = fss.save(upload.name, upload)
            file_url = fss.url(file)

            image_form_initial.description = file_url
            image_form_initial.user = current_user

            try:
                image_form_initial.save()
            except Exception as e:
                print("Error: " + str(e))

        else:
            print("Invalid Form")

        friends = get_all_friends(current_user)
        existing_rooms = get_chat_rooms(current_user)
        personal = request.user

        return render(request, './internal/home.html', {
            'personal': personal,
            'personal_details': current_user,
            'friends': friends,
            'existing_rooms': existing_rooms,
            'image_form': image_form_raw,
            'current_image': file_url
        })

    else:
        image_form = ImageMediaForm()
        try:
            current_image = Images.objects.get(user=current_user).description
        except Exception as e:
            print(str(e))
            current_image = None
        friends = get_all_friends(current_user)
        existing_rooms = get_chat_rooms(current_user)
        personal = request.user

        return render(request, './internal/home.html', {
            'personal': personal,
            'personal_details': current_user,
            'friends': friends,
            'existing_rooms': existing_rooms,
            'image_form': image_form,
            'current_image': current_image
        })


@login_required(login_url='/login/')
def get_all_friends(au: AppUser):
    try:
        response = au.friend.all()
        if response.exists():
            return response
        else:
            return []
    except response.DoesNotExist:
        return []


@login_required(login_url='/login/')
def get_chat_rooms(au: AppUser):
    try:
        response = au.rooms_set.all()
        if response.exists():
            return response
        else:
            return []
        return response
    except response.DoesNotExist:
        return []


"""
End of home page endpoints
"""

"""
Search Page Endpoints
"""


@login_required(login_url='/login/')
def search(request):
    if request.method == 'POST':
        friend = AppUser.objects.get(user=User.objects.get(pk=int(request.POST['friend_user'])))
        current_user = AppUser.objects.get(user=User.objects.get(pk=request.user.id))
        result = add_friend(current_user, friend)
        return render(request, './internal/social-search.html')

    else:
        current_user = AppUser.objects.get(user=User.objects.get(pk=request.user.id))
        response = AppUser.objects.exclude(friend=current_user).exclude(user=User.objects.get(pk=request.user.id))
        return render(request, './internal/social-search.html', {
            'friends': response
        })


@login_required(login_url='/login/')
def add_friend(current_user: AppUser, friend: AppUser):
    result = current_user.friend.add(friend)
    print(result)
    return result


"""
End of Search Page Endpoints
"""

"""
Chat Page Endpoints
"""


@login_required(login_url='/login/')
def room(request):
    errors = ""
    messages = ""
    failed = False

    if request.method == 'POST':

        create_room_form = ChatRoomForm(data=request.POST)
        current_user_id = int(request.user.id)
        current_user = AppUser.objects.get(user=User.objects.get(pk=current_user_id))


        # Check form validity
        if create_room_form.is_valid():
            room = create_room_form.save(commit=False)
            room.user = current_user
            # If room already exist
            if Rooms.objects.filter(name=request.POST['name'], user=current_user).exists():
                messages = 'Room already exist.'
                failed = True
                return render(request, './login.html', {
                    'create_room_form': create_room_form,
                    'errors': errors,
                    'message': messages,
                    'failed': failed
                })
            else:
                try:
                    room.save()
                    new_room = "/chat/" + request.POST['name'] + "/"
                    return HttpResponseRedirect(new_room)
                except Exception as e:
                    messages = e
                    failed = True
                    errors = 'Database Error'
                    return render(request, './login.html', {
                        'create_room_form': create_room_form,
                        'errors': errors,
                        'message': messages,
                        'failed': failed
                    })
    else:
        create_room_form = ChatRoomForm()
        return render(request, './internal/chat-room.html', {
            "create_room_form": create_room_form,
            'errors': errors,
            'message': messages,
            'failed': failed
        })


@csrf_exempt
@login_required(login_url='/login/')
def chat(request, room_name):

    # Get a list of history chats from user
    history_chats = Chats.objects.filter(
        room=Rooms.objects.get(name=room_name)
    ).values()

    user_raw_object = AppUser.objects.get(user=User.objects.get(pk=request.user.id))
    try:
        room_raw_object = Rooms.objects.get(name=room_name, user=user_raw_object).id
    except:
        room_raw_object = Rooms.objects.get(name=room_name).id

    history_personal = []
    history_others = []

    if len(history_chats):
        print("History Found!")
        for chat in history_chats:
            if str(chat["user_id"]) == str(AppUser.objects.get(user=User.objects.get(pk=request.user.id)).id):
                history_personal.append(chat)
            else:
                history_others.append(chat)

    return render(request, './internal/chat.html', {
        'room_name': room_name,
        'userId': request.user.id,
        'room': room_raw_object,
        'user': user_raw_object,
        'history_personal': history_personal,
        'history_others': history_others
    })


"""
End of Chat Page Endpoints
"""
