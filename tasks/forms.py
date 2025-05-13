from django import forms
from tasks.models import Task, TaskDetail

# Django Form


class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(
        widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=[], label='Assigned To')

    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id, emp.name) for emp in employees]


class StyledFormMixin:
    """Mixin to apply style to form fields"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # ✅ Corrected
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.TextInput):
                widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(widget, forms.SelectDateWidget):
                widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                widget.attrs.update({
                    'class': self.default_classes
                })

# Django Model Form
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date','assigned_to'] 
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }

class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes','asset']
