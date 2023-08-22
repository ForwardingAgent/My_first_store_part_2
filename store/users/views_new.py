from typing import Any, Dict
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required  # 5.5 не позволяет отрабатывать контроллеру пока не произведена авторизация (неавториз user не может добавить в корзину или зайти на страницу профайла пока не авторизирован)
from django.views.generic.edit import CreateView, UpdateView  # 7.6
from django.contrib.auth.views import LoginView  # 7.7
from django.contrib.messages.views import SuccessMessageMixin  # 7.8


from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):  # 7.7
    # model = ... у нас есть в settings AUTH_USER_MODEL = user.User с ней и работает LoginView
    template_name = 'users/login.html'
    form_class = UserLoginForm  # форму которую использовали для логина
    # success_url = reverse_lazy('index') не срабатывает, поэтому пропишем перенаправление в settings LOGIN_REDIRECT_URL='/'
    # ВСЁ, остальное все авторизация (с помощью username и password) и проверки происходят сами.
    title = 'Store - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):  # 7.6, 7.8 SuccessMessageMixin ВСЕГДА ПИШУТСЯ ПЕРВЫМИ!!
    model = User
    form_class = UserRegistrationForm  # какую форму использовать для регистрации UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')  # куда перенаправлять
    success_message = 'Поздравляем, вы успешно зарегистрировались!'  # 7.8 Mixins
    title = 'Store - Регистрация'

    # 7.8 def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # get_context_data можно использовать т.к. наследуется от ContextMixin
    #     context = super(UserRegistrationView, self).get_context_data(**kwargs)  # cоздает словарь | сначала через super вызываем родительский метод, чтобы он выполнился, и ниже добавляем наши ключи в словарь (т.е. переопределили род.метод)
    #     context['title'] = 'Store - Регистрация'
    #     return context


class UserProfileView(TitleMixin, UpdateView):  # 7.6, 7.8 TitleMixin
    model = User
    form_class = UserProfileForm  # какую форму использовать для профиля UserProfileForm (форму сами делали)
    template_name = 'users/profile.html'
    # success_url = reverse_lazy('users:profile') вместо этого берем готовую ф-ю get_success_url и переопределяем (ниже) тк у нас в urls.py приходит еще и id (profile/<int:pk>/)
    title = 'Store - Профиль'  # 7.8

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=(self.object.id))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # get_context_data можно использовать т.к. наследуется от ContextMixin
        context = super(UserProfileView, self).get_context_data(**kwargs)  # cоздает словарь | сначала через super вызываем родительский метод, чтобы он выполнился, и ниже добавляем наши ключи в словарь (т.е. переопределили род.метод)
        # 7.8 context['title'] = 'Store - Профиль'  # дополняем словарь своими данными
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


# def logout(request):  # 4.14  7.7 удалим тут, и добавим встроеный LogoutView.as_view в urls и в settings LOGOUT_REDIRECT_URL
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# 7.7  4.7 урок
# def login(request):  # при первом входе на страницу /users/login/ срабатывает GET запрос и преходит ниже на else которая return пустую форму для заполнения 'users/login.html'
#                      # при заполнении формы и нажатии Авторизоваться срабатывает if, т.к. это POST запрос
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)  # заполняем класс UserLoginForm данными из POST запроса, request.POST-это словарь
#         if form.is_valid():  # тут происходит AUDIT (контроль)
#             username = request.POST['username']  # если данные прошли валидацию то из словаря request.POST достаем username
#             password = request.POST['password']  # ... password
#             user = auth.authenticate(username=username, password=password)  # после проверки,  тут происходит AUTHENTICATION (подтверждение личности) надо достать пользователя из БД и понять существует ли он
#             if user:  # == True
#                 auth.login(request, user)  # если нашли в БД тут происходит AUTHORISATION (Разрешение)
#                 return HttpResponseRedirect(reverse('index'))  # перенаправление посе регистрации на  главную страниц
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


# 7.6 def registration(request):  # 4.11
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()  # пишем save для формы а он уже вызовет save для объектов и сохранит все в БД (first_name.save(), last_name.save() и тд)
#             messages.success(request, 'Поздравляем, вы успешно зарегистрировались!')  # 4.13 
#             return HttpResponseRedirect(reverse('users:login'))  # перенаправляем на старницу авторизации
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


# 7.6 @login_required  # декоратор 5.5, можно тут прописать (login_url='/users/login/')чтобы перенаправлять на регистрацию, но пропишем это все в settings внизу
# def profile(request):
#     if request.method == 'POST':  # 4.12 добавялем if для варианта если user меняет first_name и last_name в профиле в лич.кабинете
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)  # instance это ТЕ first_name и last_name КОТОРЫЕ мы меняем в профиле в лич.кабинете,
#         # а data это данные НА КОТОРЫЕ мы меняем, которые приходят когда User меняет first_name и last_name
#         # files передает изображение загруженное User'ом
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))  # возвращаем на ту же страницу профиля
#     else:
#         form = UserProfileForm(instance=request.user)  # 4.12 добавляем instance с данными user чтобы в личн.кабинете в поля небыли пустыми
#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),  # 5.3, а в 5.4 all() изменили не filter(user...) чтобы разделить товары по разным user'ам
#     }
#     return render(request, 'users/profile.html', context)

