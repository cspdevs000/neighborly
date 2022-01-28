from django.urls import path
from .views import PostView, ReplyView, AddBuilding, AddOccupantsView, ConfirmBuilding, ProfileView, PostEditView, PostDeleteView, ReplyEditView, ReplyDeleteView, ProfileEditView, ProfileDeleteView, send_add_request, approve_request
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('addbuilding/', AddBuilding.as_view(), name='addbuilding'),
    path('addoccupants/', AddOccupantsView.as_view(), name='addoccupants'),
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
    path('send_add_request/<int:userID>/', send_add_request, name='send_add_request'),
    path('approve_request/<int:requestID>/', approve_request, name='approve_request'),
]