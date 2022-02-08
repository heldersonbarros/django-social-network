from multiprocessing import context
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import json

from .models import User
from posts.models import Post
from .forms import LoginForm, UserCreateForm, UserUpdateForm, UserPasswordChangeForm
from posts.views import LikeMixin, PaginationMixin

class UserLogin(LoginView):
    extra_context = {"title": "login"}
    redirect_authenticated_user = True
    success_url = reverse_lazy("posts:index")
    form_class = LoginForm

class UserCreate(CreateView):
    extra_context = {"title": "register"}
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("posts:index")
    redirect_authenticated_user=True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("posts:index")
        return super().dispatch(request, *args, **kwargs)

class UserDetail(LoginRequiredMixin,LikeMixin, PaginationMixin, ListView):
    model = Post
    template_name = "accounts/user_detail.html"
    paginate_by = 15

    def get_object(self):
        return get_object_or_404(User, username = self.kwargs["username"])

    def get_queryset(self):
        self.object = self.get_object()
        queryset = self.object.post_set.order_by("-created_at")
        return super().get_queryset(queryset)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.object

        return context

class UserFollowers(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 8
    extra_context = {"title": "Followers"}

    def get_queryset(self):
        self.object = User.objects.get(username=self.kwargs["username"])
        queryset = self.object.followers.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.object

        return context

class UserFollowing(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 8
    extra_context = {"title": "Following"}

    def get_queryset(self):
        self.object = User.objects.get(username=self.kwargs["username"])
        queryset = self.object.following.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.object

        return context

class UserUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("accounts:update")
    success_message = "The information was updated successfully"
    extra_context = {"form_type": "update"}

    def get_object(self, queryset=None):
        return self.request.user

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("posts:change_password")
    success_message = "Your password was updated successfully"
    extra_context = {"form_type": "password_change"}

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/settings.html"
    success_url = reverse_lazy("posts:login")
    success_message = "Account was deleted successfully"
    extra_context = {"form_type": "delete"}

    def get_object(self, queryset=None):
        return self.request.user

@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def follow(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user = User.objects.get(pk=data["user_id"])
        except User.DoesNotExist:
            raise Http404("Page not found")

        added = False
        if User.objects.filter(followers=request.user, id=user.id).exists():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
            added = True
            
        return JsonResponse({'count': user.followers.count(), 'added': added})