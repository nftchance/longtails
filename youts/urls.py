from django.urls import path

from . import views

urlpatterns = [
    path('youts/', views.youts, name='youts')
]