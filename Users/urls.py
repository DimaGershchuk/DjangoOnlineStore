from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_view, RegisterUser, LoginUser, logout_user, CustomUserDetailView, CustomUserListCreateView, ProfileView, ProfileUpdateView, UserPasswordChange

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/password', UserPasswordChange.as_view(template_name='users/password_change.html'), name='password_change'),
    path('profile/password/done', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),


    # Api-endpoints
    path('api/users/', CustomUserListCreateView.as_view(), name='create-user'),
    path('api/users/<int:pk>/', CustomUserDetailView.as_view(), name='detail-user')

]