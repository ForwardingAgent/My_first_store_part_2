from django.urls import path
from django.contrib.auth.decorators import login_required  # 7.6
from django.contrib.auth.views import LogoutView  # 7.7

# from users.views import login, registration, profile, logout
from users.views import UserLoginView, UserRegistrationView, UserProfileView, EmailVerificationView  # 7.6, 7.7 7.11

# 4.7 урок
app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # адрес будет отображаться ../users/login/
    path('registration/', UserRegistrationView.as_view(), name='registration'),  # адрес будет отображаться ../users/registration/
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),  # добавили <int:pk> тк UserProfileView(UpdateView) а UpdateView принимает с id
    # везде адрес /users/... т.к. в главном (store/urls.py) path('users/'... ) а здесь уже ответвления
    path('logout/', LogoutView.as_view(), name='logout'),  # 7.7  4.14
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),  # 7.7  4.14
]
