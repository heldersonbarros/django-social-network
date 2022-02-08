from django.urls import path
from . import views

app_name = "communities"

urlpatterns = [
    path('create', views.CommunityCreate.as_view(), name="create_community"),
    path('<int:id>/', views.CommunityDetail.as_view(), name="community_page"),
    path('<int:id>/create_post/', views.CommunityPostCreate.as_view(), name="create_post_community"),
    path('<int:id>/update/', views.CommunityUpdate.as_view(), name="community_update"),
    path('<int:id>/delete/', views.CommunityDelete.as_view(), name="community_delete"),
    path('all/', views.CommunityList.as_view(), name="community_all"),
    path('join/', views.join_community, name="join"),
    path("me/", views.UserCommunities.as_view(), name="user_communities")
]