from django.urls import path
from . import views

urlpatterns = [
    path('set-reminder/', views.set_reminder, name='set_reminder'),  
]
