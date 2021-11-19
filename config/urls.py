from django.contrib import admin
from django.urls import path
from app.views import home_view, login_view, logoutUser, register_view, PostList, PostCreation, delete_post, PostUpdate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", register_view, name="register"),
    path("dashboard/", PostList.as_view(), name="dashboard"),
    path("post-creation/", PostCreation.as_view(), name="new_post"),
    path("delete/<post_id>/", delete_post, name="delete_post"),
    path("<pk>/update/", PostUpdate.as_view(), name="update_post")
]