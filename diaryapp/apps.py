from django.apps import AppConfig


class DiaryappConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'diaryapp'
    label = 'diaryapp'  # Required for router to recognize
