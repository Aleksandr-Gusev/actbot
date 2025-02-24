from django.urls import path
from .views import login_view, register_view, index_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('index/', index_view, name='index'),
    path('logout/', logout_view, name='logout'),  # Добавлен маршрут для выхода
]