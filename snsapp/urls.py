from django.urls import path
from .views import Home, MyPost, CreatePost, DetailPost, UpdatePost, DeletePost,LikeHome,  LikeDetail,TagListView ,CreateTag, SearchTagView
from django.urls import path

from . import views

urlpatterns = [
    path('', TagListView.as_view(), name='tag'),
    path('home/', Home.as_view(), name='home'),

    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),    
    path('home/tag/<str:tag_name>/', Home.as_view(), name='home-tag'),   
    path('search-tag/', SearchTagView.as_view(), name='search-tag'), 
    path('mypost/', MyPost.as_view(), name='mypost'),
    path('create/', CreatePost.as_view(), name='create'),
    path('create-tag/', CreateTag.as_view(), name='create-tag'),
    path('detail/<int:pk>', DetailPost.as_view(), name='detail'),
    path('detail/<int:pk>/update', UpdatePost.as_view(), name='update'),
    path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete'),
    path('like-home/<int:pk>', LikeHome.as_view(), name='like-home'),
    path('like-detail/<int:pk>', LikeDetail.as_view(), name='like-detail'),
]