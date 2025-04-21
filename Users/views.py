from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, LoginUserForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from rest_framework import viewsets, permissions, generics
from rest_framework.authentication import TokenAuthentication
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserCreateSerializer
from rest_framework.permissions import IsAuthenticated

def home_view(request):
    return render(request, 'home-page.html')


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        return reverse_lazy('home-page')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home-page')


def logout_user(request):
    logout(request)
    return redirect('login')


class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return CustomUserSerializer


class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
