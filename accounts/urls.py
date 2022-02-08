from django.urls import path
from django.urls import reverse_lazy

from . import views
from . import forms
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name="login"),
    path('register/', views.UserCreate.as_view(), name="register"),
    path('logout/', views.logout_view, name="logout"),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(form_class=forms.UserPasswordResetForm), name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    path('<str:username>/profile', views.UserDetail.as_view(), name="user_page"),
    path('<str:username>/profile/followers/', views.UserFollowers.as_view(), name="followers_page"),
    path('<str:username>/profile/following/', views.UserFollowing.as_view(), name="following_page"),
    path('profile/follow/', views.follow, name="follow"),
    path('profile', views.UserUpdate.as_view(), name="update"),
    path('authentication', views.PasswordChange.as_view(), name="change_password"),
    path('delete_account', views.UserDelete.as_view(), name="delete_account"),
]