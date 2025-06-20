from django.urls import path
from tasks.views import DeleteTask,TaskDetail,ViewProject,UpdateTask,CreateTask,dashboard, manager_dashboard,employee_dashboard, create_task,update_task,task_details

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('user-dashboard/', employee_dashboard, name='user-dashboard'),
    # path('create-task/', create_task, name='create-task'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('view-task/', ViewProject.as_view(), name='view-task'),
    # path('task/<int:task_id>/details/',task_details,name='task-details'),
    path('task/<int:task_id>/details/',TaskDetail.as_view(),name='task-details'),
    # path('update-task/<int:id>/', update_task, name='update-task'),
    path('update-task/<int:id>/', UpdateTask.as_view(), name='update-task'),
    # path('delete-task/<int:id>/',delete_task,name='delete-task'),
    path('delete-task/<int:id>/',DeleteTask.as_view(),name='delete-task'),
    path('dashboard/', dashboard, name='dashboard'),
]