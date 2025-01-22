from django.urls import path
from tasks.views import show_task

urlpatterns=[
    path('show-task/',show_task)
]