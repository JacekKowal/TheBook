from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login-view'),
    path('register/', views.CreateUserView.as_view(), name='register-view'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile-view'),
    path('follow/<int:pk>', views.FollowView.as_view(), name='follow-view'),
    path('unfollow/<int:pk>', views.UnfollowView.as_view(), name='unfollow-view'),
    path('send_message/<int:pk>', views.SendMessageView.as_view(), name='send-message'),
    path('messages/', views.MessagesView.as_view(), name='messages-view'),
]

