from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Building

def index(request):
    return HttpResponse("Hello, world. You're at the neighborly test landing page.")

def home(request):
    building_list = Building.objects.all()
    context = {
        'building_list': building_list,
    }
    return render(request, 'neighborly/home.html', context)

def building(request, building_id):
    building = get_object_or_404(Building, pk=building_id)
    return render(request, 'neighborly/building.html', {'building': building})



#todo
#figure out how to use built in user model to app's models
#or figure out how to make created user model reflect auth

#make homepage / login screen
#add building search to home page
#add request to be added to building button
#only display building info if user is confirmed
#add send invitation functionality for building admin

#style home page
#style building page / posts & replies