from django.urls import path
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

app_name = "posts"

urlpatterns = [
    path('', views.PostList.as_view(), name="index"),
    path('explore', views.Explore.as_view(), name="explore"),
    path('post/<int:id>', views.PostDetail.as_view(), name="detail"),
    path('post/<int:id>/comments/', views.load_comments, name="load_comments"),
    path('post/<int:pk>/delete', views.PostDelete.as_view(), name="delete"),
    path('create_post', views.PostCreate.as_view(), name="create_post"),
    path('like_post', views.like_post, name="like_post"),
    path('about', views.about, name="about"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)