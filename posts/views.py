from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.db.models import Exists, OuterRef
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import FormMixin

import json
from datetime import date, timedelta

from . serializers import PostSerializer, CommentSerializer
from . models import Post, Comment, Like
from . forms import PostForm, CommentForm
from accounts.models import User

class PaginationMixin:
    def render_to_response(self, context, **response_kwargs):
        if self.request.accepts('text/html'):
            return super().render_to_response(context, **response_kwargs)
        else:
            if self.request.user.is_authenticated:
                user = self.request.user
            else:
                user = None
                
            serializer = PostSerializer(context['post_list'], context={"user": user}, many=True)
            return JsonResponse({"posts": serializer.data, "has_next": context["page_obj"].has_next()}, safe=False)

class LikeMixin:
    def get_queryset(self, queryset):
        return queryset.annotate(
            is_liked=  Exists(Like.objects.filter(
                user_id=self.request.user.id,
                post_id=OuterRef('id')
            ))
        )

class PostList(LoginRequiredMixin, LikeMixin, PaginationMixin, ListView):
    model = Post
    paginate_by = 15
    extra_context = {"title": "Homepage"}

    def get_queryset(self):
        following = self.request.user.following.all()
        communities = self.request.user.community_set.all()
        
        following_posts = Post.objects.filter(user__id__in=following).order_by("-created_at")
        communities_posts = Post.objects.filter(community__id__in=communities).exclude(user=self.request.user).order_by("-created_at")

        queryset = following_posts | communities_posts

        return super().get_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = self.request.user.following.all()
        print(following)
        context["follow_recommendation"] = User.objects.exclude(id__in=following).exclude(id=self.request.user.id)[:3]
        return context

class Explore(LoginRequiredMixin, LikeMixin, PaginationMixin, ListView):
    model = Post
    paginate_by = 15
    extra_context = {"title": "Explore"}

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(user__username__icontains=q) | Q(community__title__icontains=q))
        else:
            startdate = date.today()
            enddate = startdate + timedelta(days=6)
            queryset = queryset.filter(created_at__range=[startdate, enddate]).annotate(count=Count("like")).order_by('-count').exclude(user=self.request.user)

        return super().get_queryset(queryset.order_by("-created_at"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = self.request.user.following.all()
        context["follow_recommendation"] = User.objects.exclude(id__in=following).exclude(id=self.request.user.id)[:3]
        return context
            
class PostDetail(LoginRequiredMixin, LikeMixin, FormMixin, DetailView):
    model = Post
    context_object_name = "post"
    pk_url_kwarg = 'id'
    form_class = CommentForm

    def get_object(self):
        return self.get_queryset().first()

    def get_queryset(self):
        queryset = self.model.objects.filter(id= self.kwargs[self.pk_url_kwarg])
        return super().get_queryset(queryset)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.get_object().comment_set.all()[:10]
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy('posts:detail', kwargs = {'id': self.get_object().id})

class PostCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    success_message = "Post was created successfully"

    def get_success_url(self):
        return reverse_lazy("accounts:user_page", args=[self.request.user.username])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts:index")

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id= self.kwargs["pk"])

        if self.request.user != post.user:
            return redirect("posts:index")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("accounts:user_page", args=[self.request.user.username])

@login_required
def load_comments(request, id):
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        raise Http404("Page not found")

    p = request.GET.get("page", 1)

    comments = Comment.objects.filter(post = post)

    pagination = Paginator(comments, 10)

    try:
        page = pagination.page(p)
        serializer = CommentSerializer(page, many=True)
        return JsonResponse({"comments": serializer.data, "has_next": page.has_next()}, safe=False)
    except EmptyPage:
        pass

@login_required
def about(request):
    return render(request, "posts/about.html")

@login_required
def like_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            post = Post.objects.get(pk=data["post_id"])
        except Post.DoesNotExist:
            raise Http404("Page not found")

        like = Like.objects.filter(post=post, user=request.user)
        added = False
        if like:
            like.delete()
        else:
            like = Like(user=request.user, post=post)
            like.save()
            added = True

    return JsonResponse({'count': post.like_set.count(), 'added': added})