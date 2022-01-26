from django.urls import path
from .views import PostView, ReplyView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('building/<int:building_id>/', PostView.as_view(), name='building'),
    path('post/<int:post_id>/', ReplyView.as_view(), name='post')
]