from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):

    SELF_EMPLOYED = 'Self-employed'
    IP = 'IP'
    
    TYPE_OF_WORKER_CHOICES = [
        (SELF_EMPLOYED, 'Самозанятый'),
        (IP, 'Индивидуальный предприниматель'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user_second_name = models.CharField(max_length=100)
    user_surname = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)  # email должен быть уникальным
    user_town = models.CharField(max_length=100)
    type_of_worker = models.CharField(max_length=100, choices=TYPE_OF_WORKER_CHOICES)

    def __str__(self):
        return self.user.username
    

class MyModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='records', null=True, blank=True)
    number_contact = models.CharField(max_length=80) #null=True - если можно хранить нулл, blank=True - если разрешаем хранить пустую ячейку
    date_contact = models.CharField(max_length=10)
    number_act = models.IntegerField()
    project= models.CharField(max_length=150)
    stavka = models.FloatField()
    date_start = models.CharField(max_length=10)
    date_end = models.CharField(max_length=10)
    time_of_work = models.FloatField()
    name_of_work = models.CharField(max_length=80)
    result_of_work = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)  # Автоматическая запись текущей даты и времени
    total = models.FloatField(max_length=30)
    status = models.CharField(max_length=30, default='process')
    text_error = models.CharField(max_length=150, default='0')

    def save(self, *args, **kwargs):
        # Перед сохранением вычисляем total как произведение price и quantity
        self.total = self.stavka * self.time_of_work
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Выводим все поля в строковом представлении
        return f"{self.number_contact}, {self.date_contact}, {self.number_act}, {self.project}, {self.stavka}, {self.date_start}, {self.date_end},{self.time_of_work}, {self.name_of_work}, {self.result_of_work}"