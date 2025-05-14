from django import template
from datetime import datetime
from django.utils import timezone

register=template.Library() # This is for register the library and rigister will be act like a object.

@register.filter # By calling this object i can use it like a decoretor
def humanized_date(value):
    if value:
        today=datetime.now().date()
        value=timezone.localtime(value)
        if value.date()==today:
            return f"Today at {value.strftime('%I:%M %p')}"
        elif value.date()==today.replace(day=today.day-1):
            return f"Yesterday at {value.strftime('%I %M %p')}"
        else:
            return f"{value.date().strftime('%B %d')},value.strftime('%I %M %p')"
    return 'No login record available'