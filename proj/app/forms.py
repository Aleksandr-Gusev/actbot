from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, MyModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator

class RegistrationForm(forms.Form):
    user_name = forms.CharField(max_length=100, label="Имя")
    user_second_name = forms.CharField(max_length=100, label="Отчество")
    user_surname = forms.CharField(max_length=100, label="Фамилия")
    user_email = forms.EmailField(label="Электронная почта")
    user_town = forms.CharField(max_length=100, label="Город")
    type_of_worker = forms.CharField(max_length=100, label="Тип работника")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Подтверждение пароля")

    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    # Если нужно, можно добавить дополнительные валидации
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Дополнительно можно настроить виджет для поля type_of_worker, если нужно
        # Устанавливаем стиль для поля type_of_worker, чтобы сделать его шире
        self.fields['type_of_worker'].choices = CustomUser.TYPE_OF_WORKER_CHOICES
        self.fields['type_of_worker'].widget = forms.Select(attrs={'style': 'width: 300px;'})
    


    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['user_email'].split('@')[0],  # Генерация username из email
            email=self.cleaned_data['user_email'],
            password=self.cleaned_data['password1']
        )

        # Сохраняем дополнительные данные в CustomUser
        custom_user = CustomUser(
            user=user,
            user_name=self.cleaned_data['user_name'],
            user_second_name=self.cleaned_data['user_second_name'],
            user_surname=self.cleaned_data['user_surname'],
            user_email=self.cleaned_data['user_email'],
            user_town=self.cleaned_data['user_town'],
            type_of_worker=self.cleaned_data['type_of_worker']
        )
        custom_user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")

""" # Регулярное выражение для проверки даты в формате YYYY-MM-DD
date_regex = r'^\d{4}-\d{2}-\d{2}$'  # пример: 2025-01-24 """
class MyModelForm(forms.ModelForm):     #Мы создаём форму, которая будет связана с моделью MyModel с помощью класса ModelForm. Это позволяет Django автоматически сгенерировать форму на основе полей модели.
    class Meta:
        model = MyModel                 #это означает, что форма будет работать с моделью MyModel.
        fields = ['number_contact', 'date_contact', 'number_act', 'project', 'stavka', 'date_start', 'date_end', 'time_of_work', 'name_of_work', 'result_of_work']         #указывает, какие именно поля из модели будут включены в форму.
    
    # Применяем регулярное выражение для валидации даты
    #date_start = forms.CharField(validators=[RegexValidator(regex=date_regex, message="Введите дату в формате YYYY-MM-DD")],required=True)
    #date_end = forms.CharField(validators=[RegexValidator(regex=date_regex, message="Введите дату в формате YYYY-MM-DD")],required=True)  
    date_start = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Используем виджет для даты
    date_end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Используем виджет для даты 
    date_contact = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Используем виджет для даты 

    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем пользователя из аргументов
        super().__init__(*args, **kwargs)
        self.user = user  # Сохраняем пользователя для дальнейшего использования