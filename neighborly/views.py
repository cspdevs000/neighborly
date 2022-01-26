from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from .models import Building, ExtendUser, Post, Reply
from django.contrib.auth.models import User
from neighborly.forms import PostForm, ReplyForm
from django.views import View

def index(request):
    return render(request, 'neighborly/index.html')

def home(request):
    current_user = request.user
    print('current_user -->', current_user)
    if ExtendUser.objects.filter(user__username = request.user):
        building = ExtendUser.objects.filter(user__username = request.user)[0].building
        print('building -->', building)
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

class PostView(View):
    def get(self, request, building_id, *args, **kwargs):
        current_user = request.user
        print('current_user -->', current_user)
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
        context = {
            'building': building,
            'post_list': posts,
            'form': form,
        }
        return render(request, 'neighborly/building.html', context)

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
        context = {
            'post': post,
            'reply_list': reply,
            'replyform': replyform,
        }
        return render(request, 'neighborly/post.html', context)


#todo
#add building form page with cooresponding button on home page
#add send invitation functionality for building admin
#add city and state to building model
#add building search to home page
#if search comes up empty, prompt user to add building
#add request to be added to building button
#pinned posts

#style home page
#style building page / posts & replies
#clean up signup / login / logout pages