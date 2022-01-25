from django.urls import path
from .views import PostView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    # path('building/<int:building_id>/', views.building, name='building'),
    # path('building/<int:building_id>/', views.buildingpost, name='postbuilding'),
    path('building/<int:building_id>/', PostView.as_view(), name= 'building')
]