from django import template
import datetime

register = template.Library()

@register.filter
def format_duration(value):
    try:
        if isinstance(value, str):
            value = datetime.timedelta(seconds=float(value.split(':')[0]) * 3600 +
                                       float(value.split(':')[1]) * 60 +
                                       float(value.split(':')[2].split('.')[0]))
        minutes = int(value.total_seconds() // 60)
        seconds = int(value.total_seconds() % 60)
        return f"{minutes}m {seconds}s"

    except:
        return value

# from django.utils.timezone import localtime

# local_start = localtime(entry.strtime)


