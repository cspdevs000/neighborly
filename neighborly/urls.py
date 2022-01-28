from django.urls import path
from .views import PostView, ReplyView, AddBuilding, ConfirmBuilding, ProfileView, PostEditView, PostDeleteView, ReplyEditView, ReplyDeleteView, ProfileEditView, ProfileDeleteView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('addbuilding/', AddBuilding.as_view(), name='addbuilding'),
    path('confirmbuilding/', ConfirmBuilding.as_view(), name='confirmbuilding'),
    path('building/<int:building_id>/', PostView.as_view(), name='building'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='postedit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='postdelete'),
    path('post/<int:post_id>/', ReplyView.as_view(), name='post'),
    path('reply/edit/<int:pk>/', ReplyEditView.as_view(), name='replyedit'),
    path('reply/delete/<int:pk>/', ReplyDeleteView.as_view(), name='replydelete'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profileedit'),
    path('profile/delete/<int:pk>/', ProfileDeleteView.as_view(), name='profiledelete'),
]