from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task
# @receiver(post_save,sender=Task)
# def notify_task_creation(sender,instance,created,**kwargs):
#     print("sender:",sender),
#     print("instace:",instance),
#     print("K:",kwargs),
#     print("Created:",created)
#     if created:
#         instance.is_completed=True
#         instance.save()

# @receiver(pre_save,sender=Task)
# def notify_task_creation(sender,instance,**kwargs):
#     print("sender:",sender),
#     print("instace:",instance),
#     print("K:",kwargs),
    
#     instance.is_completed=True

@receiver(m2m_changed,sender=Task.assigned_to.through)
def notify_employess_on_task_creation(sender,instance,action,**kwargs):
    if action=='post_add':
        assigned_emails=[emp.email for emp in instance.assigned_to.all()]

        send_mail(
            "New Task Assigned",
            f"You have heen assigned to the task: {instance.title}",
            "easin562050@gmail.com",
            assigned_emails,
            # fail_silently=False,
        )

@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if hasattr(instance, 'details'): 
        instance.details.delete()
        print("Delete successfully")
