from django.urls import path
from django.contrib.auth.decorators import login_required  # 7.6

from users.views import login, registration, profile, logout
from users.views_new import login, UserRegistrationView, UserProfileView, logout  # 7.6

# 4.7 урок
app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),  # адрес будет отображаться ../users/login/
    path('registration/', UserRegistrationView.as_view(), name='registration'),  # адрес будет отображаться ../users/registration/
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),  # добавили <int:pk> тк UserProfileView(UpdateView) а UpdateView принимает с id
    # везде адрес /users/... т.к. в главном (store/urls.py) path('users/'... ) а здесь уже ответвления
    path('logout/', logout, name='logout'),  # 4.14
]