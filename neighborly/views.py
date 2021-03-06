from contextlib import nullcontext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from .models import AddRequest, Building, ExtendUser, Post, Reply
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from neighborly.forms import PostForm, ReplyForm, BuildingForm, ExtendBuildingForm
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView

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
        admins = results.values('creator_id')
        context = {
            'searched': searched,
            'results': results,
            'admins' : admins,
        }
        return render(request, 'neighborly/search.html', context)
    else:
        return render(request, 'neighborly/search.html')


class AddBuilding(View):
    def get(self, request, *args, **kwargs):
        print('current user --->', request.user.id)
        if request.user == 'AnonymousUser':
            current_user = ExtendUser.objects.filter(user__username = request.user)[0]
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
        extendbuildingform = ExtendBuildingForm(request.POST)
        current_user = User.objects.filter(id = request.user.id)[0]
        print('USER!! -->', current_user)
        if buildingform.is_valid():
            new_building = buildingform.save(commit=False)
            new_building.creator = current_user
            new_building.save()
        if extendbuildingform.is_valid():
            new_user_building = extendbuildingform.save(commit=False)
            new_user_building.building_id = new_building.id
            new_user_building.user_id = request.user.id
            new_user_building.save()
        return redirect('confirmbuilding')

class ConfirmBuilding(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'neighborly/confirmbuilding.html')


class PostView(View):
    def get(self, request, building_id, *args, **kwargs):
        if ExtendUser.objects.filter(user__username = request.user)[0].building_id == building_id:
            user = request.user
            building = get_object_or_404(Building, pk=building_id)
            posts = Post.objects.filter(building = building_id).order_by('-pub_date')[:5]
            form = PostForm()
            replyform = ReplyForm()
            context = {
                'user': user,
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
        posts = Post.objects.filter(building = building_id).order_by('-pub_date')[:5]
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.building = building
            new_post.save()
            form = PostForm()
        return HttpResponseRedirect(reverse('building', args=(building.id,)))

class PostEditView(UpdateView):
    model = Post
    fields = ['body']
    template_name = 'neighborly/postedit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post', args=(pk,))

class PostDeleteView(DeleteView, SuccessMessageMixin):
    model = Post
    template_name = 'neighborly/postdelete.html'
    success_url = reverse_lazy('home')
    success_message = 'Profile was successfully deleted'

class LeaveBuilding(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'neighborly/leavebuilding.html')

    def post(self, request, *args, **kwargs):
        extendbuildingform = ExtendBuildingForm(request.POST)
        if extendbuildingform.is_valid():
            new_user_building = extendbuildingform.save(commit=False)
            new_user_building.building_id = None
            new_user_building.user_id = request.user.id
            new_user_building.save()
        return redirect('home')



class ReplyView(View):
    def get(self, request, post_id, *args, **kwargs):
        building = ExtendUser.objects.filter(user__username = request.user)[0].building
        post = get_object_or_404(Post, pk=post_id)
        reply = Reply.objects.filter(post = post_id).order_by('-pub_date')
        replyform = ReplyForm()
        context = {
            'building': building,
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

class ReplyEditView(UpdateView):
    model = Reply
    fields = ['body']
    template_name = 'neighborly/replyedit.html'

    def get_success_url(self):
        return reverse_lazy('home')

class ReplyDeleteView(DeleteView):
    model = Reply
    template_name = 'neighborly/replydelete.html'
    success_url = reverse_lazy('home')

class ProfileView(View):
    def get(self, request, user_id, *args, **kwargs):
        print('imageURL --->', request.user.profile.image)
        profile = ExtendUser.objects.get(pk=user_id)
        user = profile.user
        context = {
            'user': user,
            'profile': profile
        }
        return render (request, 'neighborly/profile.html', context)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExtendUser
    fields = ['name', 'image']
    template_name = 'neighborly/profileedit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', args=(pk,))

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class ProfileDeleteView(DeleteView, SuccessMessageMixin):
    model = User
    template_name = 'neighborly/profiledelete.html'
    success_message = "Profile was successfully deleted"
    success_url = reverse_lazy('index')

def send_add_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    add_request, created = AddRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        messages.success(request, 'Request has been sent.')
        return redirect('home')
    else:
        return HttpResponse('already requested to be added to this building')

def approve_request(request, requestID):
    add_request = AddRequest.objects.get(id=requestID)
    from_user = AddRequest.objects.get(id=requestID).from_user
    to_user = AddRequest.objects.get(id=requestID).to_user
    if add_request.to_user == request.user:
        add_request.to_user.profile.occupants.add(add_request.from_user.profile)
        add_request.from_user.profile.occupants.add(add_request.to_user.profile)
        from_user.profile.building = to_user.profile.building
        from_user.save()
        add_request.delete()
        messages.success(request, 'Request has been approved.')
        return HttpResponseRedirect(reverse('addoccupants', args=(request.user.profile.building_id,)))
    else:
        return HttpResponse('new occupant unable to be added, try again')

def transfer_admin(request, occupantID):
    building = get_object_or_404(Building, pk=request.user.profile.building_id)
    to_user = get_object_or_404(User, pk=occupantID)
    if building == request.user.profile.building:
        building.creator = to_user
        building.save()
        messages.success(request, 'Roles have been transferred.')
        return redirect('home')
    else:
        return HttpResponse('unable to transfer roles')

class AddOccupantsView(View):
    def get(self, request, building_id, *args, **kwargs):
        building = get_object_or_404(Building, pk=building_id)
        occupants = ExtendUser.objects.filter(occupants = building_id)
        # print('occupants~!! --->', occupants[0].user_id)
        requests = AddRequest.objects.all()
        context = {
            'occupants': occupants,
            'building': building,
            'requests': requests
        }
        return render(request, 'neighborly/addoccupants.html', context)


#todo
#find / replace navbar dropdown icon
#change font?
#try to figure out how to remove occupant association upon leaving building
#add delete user to building admin page
#add to portfolio
#fix portfolio redirect
#add portfolio url to resume
#post likes?
#DMs?

#stretch goals
#add search user / send invitation functionality for building admin
#handle creator leaving building
#pinned posts
#fix default photo in cloudinary