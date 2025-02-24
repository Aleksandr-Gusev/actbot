from django.shortcuts import render, redirect           # для рендеринга шаблонов и перенаправлений
from django.contrib.auth import login, authenticate     # для работы с аутентификацией
from django.contrib import messages                     # для отображения сообщений об ошибках и успехах
from .forms import RegistrationForm, LoginForm, MyModelForm
from django.contrib.auth import logout as auth_logout   # импортируем формы для логина и регистрации
from django.contrib.auth.decorators import login_required   # декоратор для защиты представлений от неавторизованных пользователей
from .models import CustomUser,MyModel
from .core_sc.script import get_data_from_jira
from datetime import datetime

# Представление для страницы логина
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # Если пользователь уже авторизован, редирект на главную страницу

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)    # создаем форму, передавая данные из POST-запроса
        if form.is_valid():                             # если форма валидна (логин и пароль правильные)
            user = form.get_user()                      # получаем пользователя, если форма прошла валидацию
            login(request, user)                        # выполняем вход пользователя
            return redirect('index')                    # После успешного входа на главную страницу
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = LoginForm()                              # если запрос не POST (то есть страница загружена впервые), создаем пустую форму

    return render(request, 'login.html', {'form': form})    # рендерим шаблон с формой логина

# Представление для страницы регистрации
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя и CustomUser
            messages.success(request, "Регистрация прошла успешно! Теперь можете войти.")
            return redirect('login')  # Перенаправляем на страницу входа
        else:
            messages.error(request, "Ошибка регистрации. Проверьте форму.")
            print(form.errors)  # Для отладки ошибок формы
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def index_view(request):
    if request.method == 'POST': #Если запрос POST (то есть форма была отправлена), мы создаем экземпляр формы с данными из запроса request.POST.
        form = MyModelForm(request.POST, user=request.user.customuser) # передаем CustomUser
        #form = MyModelForm(request.POST) # передаем CustomUser
        
        if form.is_valid():
            #form.save()
            
            mymodel_instance = form.save(commit=False) #это получается текущая строка в БД
            mymodel_instance.user = request.user.customuser  # Привязываем пользователя
            mymodel_instance.save()

            # Получаем текущего пользователя
            current_user = request.user
        
            # Получаем объект CustomUser, связанный с этим пользователем
            custom_user = current_user.customuser
        
            # Теперь можно получить данные из customuser
            user_name = custom_user.user_name
            user_second_name = custom_user.user_second_name
            user_surname = custom_user.user_surname
            user_email = custom_user.user_email
            user_town = custom_user.user_town
            type_of_worker = custom_user.type_of_worker
            print(f'{user_name} {user_surname} {type_of_worker}')
            
            # ---------------------скрипт---------------------
            project = request.POST.get('project')
            stavka = request.POST.get('stavka')
            date_start = request.POST.get('date_start')
            date_end = request.POST.get('date_end')
            time_of_work = request.POST.get('time_of_work')
            number_act = request.POST.get('number_act')
            number_contract = request.POST.get('number_contact')
            date_contract = request.POST.get('date_contact')
            name_of_work = request.POST.get('name_of_work')
            result_of_work = request.POST.get('result_of_work')
            
            
            status_rec = get_data_from_jira(project, stavka, date_start, date_end, time_of_work, user_name, user_second_name, user_surname, user_email, user_town, type_of_worker, number_act, number_contract, date_contract, name_of_work, result_of_work)
            #-----------------------------------------------------
            #здесь нужно передать статус запроса.
            
            mymodel_instance.status = status_rec[0]
            mymodel_instance.text_error = status_rec[1]
            mymodel_instance.save()
            return redirect('/')  # перенаправление на страницу успеха
            
    else:
        form = MyModelForm()
    
    if hasattr(request.user, 'customuser'):
        # Получаем записи для текущего пользователя последние 10
        records = MyModel.objects.filter(user=request.user.customuser).order_by('-created_at')[:10]
    else:
        records = []  # Если у пользователя нет записи в CustomUser
    #records = MyModel.objects.all().order_by('-created_at')         # Получаем все записи из таблицы
    #передача ФИО
    user_name = request.user.customuser.user_name
    user_second_name = request.user.customuser.user_second_name
    user_surname = request.user.customuser.user_surname
    return render(request, 'index.html', {'form': form, 'records': records, 'user_name':user_name, 'user_second_name':user_second_name, 'user_surname':user_surname})
    #return render(request, 'index.html')


# Выход
def logout_view(request):
    auth_logout(request)   # вызываем функцию logout для выхода пользователя из аккаунта
    return redirect('login')  # Перенаправление на страницу логина

""" def success(request):
    return render(request, 'success.html') """
