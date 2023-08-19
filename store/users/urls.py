from django.urls import path

from users.views import login, registration, profile, logout

# 4.7 урок
app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),  # адрес будет отображаться ../users/login/
    path('registration/', registration, name='registration'),  # адрес будет отображаться ../users/registration/
    path('profile/', profile, name='profile'),  # адрес будет отображаться ../users/profile/
    # везде адрес /users/... т.к. в главном (store/urls.py) path('users/'... ) а здесь уже ответвления
    path('logout/', logout, name='logout'),  # 4.14
]