from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, LoginUserForm, ProfileForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from rest_framework import viewsets, permissions, generics
from .models import CustomUser
from Products.models import Category
from .serializers import CustomUserSerializer, CustomUserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from Orders.models import Order, OrderItem


def home_view(request):
    categories = Category.objects.all()
    return render(request, 'home-page.html', {'categories': categories})


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse_lazy('home-page')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home-page')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "users/password_change_form.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['user'] = self.request.user
        ctx['orders'] = Order.objects.filter(user=user).prefetch_related(Prefetch('items', queryset=OrderItem.objects.select_related('product'), to_attr='items_prefetched')).order_by('-created_at')
        return ctx


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'users/profile-edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return CustomUserSerializer


class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
