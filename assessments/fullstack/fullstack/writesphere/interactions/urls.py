from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('rate/<int:post_id>/', views.rate_post, name='rate_post'),
    path('following/', views.user_following, name='following'),
    path('followers/', views.user_followers, name='followers'),
]
