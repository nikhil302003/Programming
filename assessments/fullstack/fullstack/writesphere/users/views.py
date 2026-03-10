from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm
from blog.models import Post

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('users:dashboard')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = 'login'
        return kwargs

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('blog:home')

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! You can now login.')
        return response

class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['user_posts'] = Post.objects.filter(author=profile_user, status='published')[:5]
        context['followers_count'] = profile_user.followers.count()
        context['following_count'] = profile_user.following.count()
        
        if self.request.user.is_authenticated:
            context['is_following'] = self.request.user.following.filter(
                following=profile_user
            ).exists()
        
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.request.user.username})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself!")
        return redirect('users:profile', username=username)
    
    from interactions.models import Follow
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if created:
        messages.success(request, f"You are now following {user_to_follow.username}!")
    else:
        follow.delete()
        messages.info(request, f"You have unfollowed {user_to_follow.username}.")
    
    return redirect('users:profile', username=username)

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {
        'user_posts': user_posts,
        'total_posts': user_posts.count(),
        'published_posts': user_posts.filter(status='published').count(),
        'draft_posts': user_posts.filter(status='draft').count(),
    }
    return render(request, 'users/dashboard.html', context)
