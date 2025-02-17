from django import forms
from tasks.models import Task,TaskDetail
#Django Form
class TaskForm(forms.Form):
    title=forms.CharField(max_length=250,label="Task Title")
    description=forms.CharField(widget=forms.Textarea,label="Task Description")
    due_date=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label='Assigned To')
    def __init__(self,*args,**kwargs):
        employees=kwargs.pop("employees",[])
        # print(args,kwargs)
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name)for emp in employees]

class StyleFormMixin:
    """Mixing to apply style form field"""
    default_classes="border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
    def apply_style_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",                 
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows':5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })
#Django model form
class TaskModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
       model=Task
       fields=['title','description','due_date','assigned_to']
       widgets={
           'due_date':forms.SelectDateWidget,
           'assigned_to':forms.CheckboxSelectMultiple
       }
    """Manual Widget"""   
    
    #    widgets={
    #        'title': forms.TextInput(attrs={
    #            'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
    #            "Placeholder":"Enter Task Title"
    #        }),
    #        'description':forms.Textarea(attrs={
    #            'class':"border-2 border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
    #            "Placeholder":"Describe the task"
    #        }),
    #        'due_date': forms.SelectDateWidget(attrs={
    #            'class':"border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        
    #        }),
    #        'assigned_to':forms.CheckboxSelectMultiple(attrs={
    #            'class':"space-y-2"
    #        })
    #     }
    #     #exclude=['project','is_completed','created_at','updated_at']
    """Widget using Mixing"""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widgets()

class TaskDetailModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model=TaskDetail
        fields=['priority','notes']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widgets()