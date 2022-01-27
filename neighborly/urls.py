from django.urls import path
from .views import PostView, ReplyView, AddBuilding, ConfirmBuilding, ProfileView, PostEditView, PostDeleteView
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
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
]