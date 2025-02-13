from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg
def manager_dashboard(request):
    return render(request,"dashboard/manager-dashboard.html")

def user_dashboard(request):
     return render(request, "dashboard/user-dashboard.html")

def test(request):
     context={
          "names":{"Easin","Fahad","Rasel"}
     }
     return render(request,"test.html",context)

def create_task(request):
     # employees=Employee.objects.all()
     form=TaskModelForm()#employees=employees)# For GET
     if request.method=="POST":
          form=TaskModelForm(request.POST) #For post
          if form.is_valid():
               """For Model for Data"""
               form.save()
               return render (request,'task_form.html',{"form":form,"message": "Task added successfully"})
               """For Django from Data"""
               # data=form.cleaned_data
               # title=data.get("title")
               # description=data.get("description")
               # due_date=data.get("due_date")
               # assigned_to=data.get("assigned_to")

               # task=Task.objects.create(title=title,description=description,due_date=due_date)
               
               # #Assign employee to tasks
               # for emp_id in assigned_to:
               #      employee=Employee.objects.get(id=emp_id)
               #      task.assigned_to.add(employee)
               
     context={"form":form}
     return render(request,"task_form.html",context)

def view_task(request):
     # #Retrive all data from the task model
     # tasks=Task.objects.all()
     # #retrive a specific task
     # task_3=Task.objects.get(id=1)
     # #Fetch the first task
     # first_task=Task.objects.first()
     # tasks=Task.objects.filter(status="PENDING")
     # tasks=Task.objects.filter(status="COMPLETED")
     # return render(request,"show_task.html",{"tasks":tasks, "task3":task_3,'first_task':first_task})
     # shwo the task which due day is today
     # tasks=Task.objects.filter(due_date='date.today')
     """Show the task whose proirity is low"""
     # tasks=TaskDetail.objects.exclude(priority="L")
     """Show the task that contain word paper and status pending"""
     # tasks=Task.objects.filter(title__icontains="c",status="PENDING")
     #Show the task which are pending or in-progress
     # tasks=Task.objects.filter(Q(status="PENDING")| Q(status="IN_PROGRESS"))
     # tasks=Task.objects.filter(status="kfjdf").exists()

     #Sekect realated(Foreign key and One to One field )
     # tasks=Task.objects.select_related('details'.all())
     # tasks=TaskDetail.objects.select_related('task').all()
     # tasks=Task.objects.select_related('project').all()
     """Prefetch_related (reverse Foreignkey ,manay to many)"""
     # tasks=Project.objects.prefetch_related("task_set").all()
     # tasks=Project.objects.prefetch_related("assigned_to)").all()
     # task_count=Task.objects.aggregate(num_task=Count('id'))
     projects=Project.objects.annotate(num_task=Count('task')).order_by('num_task')
     return render(request,"show_task.html",{"projects":projects})

