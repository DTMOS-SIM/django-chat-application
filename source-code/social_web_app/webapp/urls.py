from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from . import apis

urlpatterns = [
    path('', views.home),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('signup/', views.signup),
    path('lost-password/', views.lost_password),
    path('home/', views.home),
    path('search-social/', views.search),
    path('room/', views.room),
    path('chat/<str:room_name>/', views.chat),


    path('api/chat/message/', apis.send_message),
    path('api/login/', apis.user_login),
    path('api/signup/', apis.signup),
    path('api/profile/<str:pk>/', apis.get_profile),
    path('api/user/friends/<str:pk>/', apis.get_all_friends),
    path('api/friends/<str:pk>/', apis.add_friend),
    path('api/user/rooms/<str:pk>/', apis.get_chat_rooms),
    path('api/rooms/<str:pk>/', apis.add_room),
    path('api/chat/<str:user_id>/<str:room_id>/', apis.get_chat_history),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)