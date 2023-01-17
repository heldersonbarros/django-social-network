from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404
import json

from .models import Community
from posts.forms import Post
from .forms import CommunityForm
from posts.forms import PostForm
from posts.views import LikeMixin, PaginationMixin

class CommunityCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Community
    form_class = CommunityForm
    success_url = reverse_lazy("posts:index")
    success_message = "Community was created successfully"

    def get_success_url(self):
        return reverse_lazy("communities:community_page", args=[self.object.id])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()

        self.object.participants.add(self.request.user)
        return super().form_valid(form)

class CommunityPostCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    template_name = "posts/post_form.html"
    form_class = PostForm
    success_message = "Post was created successfully"

    def dispatch(self, request, *args, **kwargs):
        self.community = get_object_or_404(Community, id=self.kwargs["id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("communities:community_page", args=[self.kwargs["id"]])

    def form_valid(self, form):
        form.instance.community = self.community
        form.instance.user = self.request.user
        return super().form_valid(form)

class CommunityList(LoginRequiredMixin, ListView):
    model = Community
    paginate_by = 8

    def get_queryset(self):
        return Community.objects.order_by("-created_at")

class CommunityUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Community
    template_name = "communities/settings.html"
    form_class = CommunityForm
    extra_context = {"form_type": "update"}
    pk_url_kwarg = "id"
    success_message = "The information was updated successfully"

    def get_success_url(self):
        return self.request.path
    
    def dispatch(self, request, *args, **kwargs):
        community = get_object_or_404(Community, id= self.kwargs["id"])

        if self.request.user != community.owner:
            return redirect("posts:index")

        return super().dispatch(request, *args, **kwargs)

class CommunityDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Community
    template_name = "communities/settings.html"
    form_class = CommunityForm
    extra_context = {"form_type": "delete_community"}
    success_url = reverse_lazy("posts:index")
    pk_url_kwarg = "id"
    success_message = "Community was deleted successfully"

    def dispatch(self, request, *args, **kwargs):
        community = get_object_or_404(Community, id= self.kwargs["id"])

        if self.request.user != community.owner:
            return redirect("posts:index")

        return super().dispatch(request, *args, **kwargs)

class CommunityDetail(LoginRequiredMixin, LikeMixin, PaginationMixin, ListView):
    model = Post
    paginate_by = 15
    template_name = "communities/community_detail.html"
    extra_context = {"create": True}

    def get_object(self):
       return get_object_or_404(Community, id = self.kwargs["id"])

    # se eu posso acessar o comunity.post_set por que filtrar ? community__id=self.kwargs["id"] redundancia?
    def get_queryset(self):
        self.community = self.get_object()
        queryset = self.community.post_set.filter(community__id=self.kwargs["id"]).order_by("-created_at")
        return super().get_queryset(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["community"] = self.community
        return context

class UserCommunities(ListView):
    model = Community
    paginate_by = 8

    def get_queryset(self):
        return self.request.user.community_set.all()

@login_required
def join_community(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            community = Community.objects.get(pk=data["community_id"])
        except Community.DoesNotExist:
            raise Http404("Page not found")

        if request.user == community.owner:
            return redirect("posts:index")
        added = False
        if request.user.community_set.filter(id=community.id).exists():
            community.participants.remove(request.user)
        else:
            community.participants.add(request.user)
            added = True
            
        return JsonResponse({'count': community.participants.count(), 'added': added})