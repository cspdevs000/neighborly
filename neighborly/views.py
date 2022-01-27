from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from .models import Building, ExtendUser, Post, Reply
from django.urls import reverse
from django.contrib.auth.models import User
from neighborly.forms import PostForm, ReplyForm, BuildingForm, ExtendBuildingForm
from django.views import View

def index(request):
    return render(request, 'neighborly/index.html')

def home(request):
    current_user = request.user
    print('current_user -->', current_user)
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

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        results = Building.objects.filter(address__icontains=searched)
        context = {
            'searched': searched,
            'results': results,
        }
        return render(request, 'neighborly/search.html', context)
    else:
        return render(request, 'neighborly/search.html')


class AddBuilding(View):
    def get(self, request, *args, **kwargs):
        if request.user == 'AnonymousUser':
            current_user = ExtendUser.objects.filter(user__username = request.user)[0]
            print('current user --->', current_user)
            buildingform = BuildingForm()
            extendbuildingform = ExtendBuildingForm()
            context = {
                'buildingform': buildingform,
                'extendbuildingform': extendbuildingform
            }
            return render(request, 'neighborly/addbuilding.html', context)
        else:
            buildingform = BuildingForm()
            extendbuildingform = ExtendBuildingForm()
            context = {
                'buildingform': buildingform,
                'extendbuildingform': extendbuildingform
            }
            return render(request, 'neighborly/addbuilding.html', context)

    def post(self, request, *args, **kwargs):
        buildingform = BuildingForm(request.POST)
        if buildingform.is_valid():
            new_building = buildingform.save(commit=False)
            new_building.save()
        return redirect('confirmbuilding')

class ConfirmBuilding(View):
    def get(self, request, *args, **kwargs):
        building_confirmation = Building.objects.all()
        extendbuildingform = ExtendBuildingForm()
        context = {
            'buildingconfirmation': building_confirmation,
            'extendbuildingform': extendbuildingform
        }
        return render(request, 'neighborly/confirmbuilding.html', context)

    def post(self, request, *args, **kwargs):
        extendbuildingform = ExtendBuildingForm(request.POST)
        if extendbuildingform.is_valid():
            new_user = extendbuildingform.save(commit=False)
            new_user.user_id = request.user.id
            new_user.save()
        return render(request, 'neighborly/confirmbuilding.html')


class PostView(View):
    def get(self, request, building_id, *args, **kwargs):
        current_user = request.user
        if ExtendUser.objects.filter(user__username = request.user)[0].building_id == building_id:
            building = get_object_or_404(Building, pk=building_id)
            posts = Post.objects.filter(building = building_id).order_by('-pub_date')
            form = PostForm()
            replyform = ReplyForm()
            context = {
                'building': building,
                'post_list': posts,
                'form': form,
                'replyform': replyform,
            }
            return render(request, 'neighborly/building.html', context)
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, building_id, *args, **kwargs):
        building = get_object_or_404(Building, pk=building_id)
        posts = Post.objects.filter(building = building_id).order_by('-pub_date')
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.building = building
            new_post.save()
            form = PostForm()
        return HttpResponseRedirect(reverse('building', args=(building.id,)))

class ReplyView(View):
    def get(self, request, post_id, *args, **kwargs):
        building = ExtendUser.objects.filter(user__username = request.user)[0].building
        post = get_object_or_404(Post, pk=post_id)
        reply = Reply.objects.filter(post = post_id).order_by('-pub_date')
        replyform = ReplyForm()
        context = {
            "building": building,
            'post': post,
            'reply_list': reply,
            'replyform': replyform,
        }
        return render(request, 'neighborly/post.html', context)


    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        reply = Reply.objects.filter(post = post_id).order_by('-pub_date')
        replyform = ReplyForm(request.POST)
        if replyform.is_valid():
            new_reply = replyform.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.save()
            replyform = ReplyForm()
        return HttpResponseRedirect(reverse('post', args=(post.id,)))


#todo
#add user assocation to building created upon creation
#add profile page (mostly for admin to handle the add user to building requests)
#CRUD for user and posts
#pagination for posts
#add send invitation functionality for building admin
#pinned posts
#requests could be notifications rather than email? w approve / reject buttons?

#style home page
#style building page / posts & replies
#clean up signup / login / logout pages