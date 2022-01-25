from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from .models import Building, ExtendUser, Post, Reply
from django.contrib.auth.models import User
from neighborly.forms import PostForm
from django.views import View

def index(request):
    return HttpResponse("Hello, world. You're at the neighborly test landing page.")

# def home(request):
#     building_list = Building.objects.all()
#     print('LIST ->', building_list)
#     context = {
#         'building_list': building_list,
#     }
#     return render(request, 'neighborly/home.html', context)

def home(request):
    current_user = request.user
    if ExtendUser.objects.filter(user__username = request.user):
        building = ExtendUser.objects.filter(user__username = request.user)[0].building
        context = {
            'user': current_user,
            'building': building,
        }
        return render(request, 'neighborly/home.html', context)
    else:
        context = {
            'user': current_user,
        }
        return render(request, 'neighborly/home.html', context)

# def building(request, building_id):
#     building = get_object_or_404(Building, pk=building_id)
#     posts = Post.objects.all().order_by('-pub_date')
#     form = PostForm()

#     context = {
#         'building': building,
#         'post_list': posts,
#         'form': form,
#     }

#     return render(request, 'neighborly/building.html', context)

# def buildingpost(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('neighborly/building.html')

#     else:
#         form = PostForm()
#     return render(request, 'neighborly/building.html', {'form': form})

class PostView(View):
    def get(self, request, building_id, *args, **kwargs):
        building = get_object_or_404(Building, pk=building_id)
        posts = Post.objects.filter(building = building_id).order_by('-pub_date')
        form = PostForm()

        context = {
            'building': building,
            'post_list': posts,
            'form': form,
        }

        return render(request, 'neighborly/building.html', context)

    def post(self, request, building_id, *args, **kwargs):
        building = get_object_or_404(Building, pk=building_id)
        posts = Post.objects.filter(building = building_id).order_by('-pub_date')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.building = building
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'neighborly/building.html', context)

# def buildingpost(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             Post.body = form.cleaned_data['body']
#             Post.user = request.user
#             Post.save()
#             return HttpResponseRedirect('building/<int:building_id>/')


# def buildingpost(request):
#   if request.method == "POST":
#     if request.POST.get('body'):
#         post = Post()
#         post.body = request.POST.get('body')
#         print('FORM ---->', post.body)
#         post.save()
#     return HttpResponseRedirect('building/<int:building_id>/')


#todo
#add building search to home page
#add post and reply forms to buildings page
#add request to be added to building button
#make posts building-specific
#add send invitation functionality for building admin

#style home page
#style building page / posts & replies
#clean up signup / login / logout pages