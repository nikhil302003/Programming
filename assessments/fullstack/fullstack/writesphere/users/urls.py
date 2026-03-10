from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:username>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('follow/<slug:username>/', views.follow_user, name='follow_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
