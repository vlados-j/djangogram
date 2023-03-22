from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login_page, name='login'),
    path('register/', views.registration_page, name='register'),
    path('feed/', views.feed, name='feed'),
    path('profile/', views.my_profile, name='my_profile'),
    path('new_post/', views.create_post, name='create_post'),
    path('users_profile/', views.view_users_profile, name='users_profile'), #here should be dinamic url
    path('logout/', views.logout_user, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
