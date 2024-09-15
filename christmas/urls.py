from django.urls import path
from . import views

app_name = 'christmas'
urlpatterns = [
    path('', views.index, name='index'),
    path('secret_santa/', views.secret_santa_home, name='secret_santa_home'),
]
