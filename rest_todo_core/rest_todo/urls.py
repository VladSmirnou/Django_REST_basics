from django.urls import path
from rest_todo import views


urlpatterns = [
    path('api/v1/userposts/', views.ListCreateUserPosts.as_view()),
    path('api/v1/userpost/<int:pk>/', views.GetUpdateDeleteUserPost.as_view()),
    path('api/v1/user/', views.CreateUser.as_view()),
]
