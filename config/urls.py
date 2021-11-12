from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", register_view, name="register"),
    path("dashboard/", PostList.as_view(), name="dashboard"),
    path("post-creation/", PostCreation.as_view(), name="new_post"),
]