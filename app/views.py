from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import CreateUserForm
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

def home_view(request) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        return render(request, "index.html")

def logoutUser(request):
    logout(request)
    return redirect("login")

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data.get('username')
                if len(user) <= 10:
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)
                    return redirect('login')
                else: 
                    messages.info(request, "Username must be 10 characters or less")
        context = {'form':form}
        return render(request, 'register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)

@login_required(login_url="login")
def dashboard_view(request):
    return render(request, "dashboard.html")

class PostList(ListView, LoginRequiredMixin):
    model = Post
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class PostCreation(CreateView, LoginRequiredMixin):
    model = Post
    template_name = "new_post.html"
    fields = ['title', 'body']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreation, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
