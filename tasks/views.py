from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min,Avg
from django.contrib import messages

def manager_dashboard(request):
     # Getting task count
     # total_task=tasks.count()
     # completed_task=Task.objects.filter(status="COMPLETED").count()
     # in_progress_task=Task.objects.filter(status="IN_PROGRESS").count()
     # pending_task=Task.objects.filter(status="PENDING").count()
     # count={
     #      'total_task':,
     #      'completed_task':,
     #      'in_progress_task':,
     #      'pending_task':
     # }
     type=request.GET.get('type','all')
          
     counts=Task.objects.aggregate(
          total=Count('id'),
          completed=Count('id',filter=Q(status='COMPLETED')),
          in_progress=Count('id',filter=Q(status='IN_PROGRESS')),
          pending=Count('id',filter=Q(status='PENDING')),
          )
     
     base_query=tasks=Task.objects.select_related('details').prefetch_related('assigned_to')

     # Retriving task data
     if type=='completed':
          tasks=base_query.filter(status='COMPLETED')
     elif type=='in-progress':
          tasks=base_query.filter(status='IN_PROGRESS')
     elif type=='pending':
          tasks=base_query.filter(status='PENDING')
     elif type=='all':
          tasks=base_query.all()
     context={
          "tasks":tasks,
          "counts":counts,  
     }
     return render(request,"dashboard/manager-dashboard.html",context)



def user_dashboard(request):
     return render(request, "dashboard/user-dashboard.html")

def test(request):
     context={
          "names":{"Easin","Fahad","Rasel"}
     }
     return render(request,"test.html",context)

def create_task(request):
     # employees=Employee.objects.all()
     task_form=TaskModelForm()#employees=employees)# For GET
     task_detail_form=TaskDetailModelForm()
     if request.method=="POST":
          task_form=TaskModelForm(request.POST) #For post
          task_detail_form=TaskDetailModelForm(request.POST )
          if task_form.is_valid() and task_detail_form.is_valid():
               """For Model for Data"""
               task=task_form.save()
               task_detail=task_detail_form.save(commit=False)
               task_detail.task=task
               task_detail.save()
               messages.success(request,'Task created successfully')
               return redirect('create-task')
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
               
     context={"task_form":task_form,"task_detail_form":task_detail_form}
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

def update_task(request,id):
     # employees=Employee.objects.all()
     task=Task.objects.get(id=id)
     task_form=TaskModelForm(instance=task)#employees=employees)# For GET
     if task.details:
          task_detail_form=TaskDetailModelForm(instance=task.details)
     if request.method=="POST":
          task_form=TaskModelForm(request.POST,instance=task) #For post
          task_detail_form=TaskDetailModelForm(request.POST, instance=task.details)
          if task_form.is_valid() and task_detail_form.is_valid():
               """For Model for Data"""
               task=task_form.save()
               task_detail=task_detail_form.save(commit=False)
               task_detail.task=task
               task_detail.save()
               messages.success(request,'Task updated successfully')
               return redirect('update-task', id)
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
               
     context={"task_form":task_form,"task_detail_form":task_detail_form}
     return render(request,"task_form.html",context)

def delete_task(request,id):
     if request.method=="POST":
          task=Task.objects.get(id=id)
          task.delete()
          messages.success(request,"The task is deleted")
          return redirect('manager-dashboard')
     else:
          messages.error(request,"Something went wrong")
          return redirect('manager-dashboard')