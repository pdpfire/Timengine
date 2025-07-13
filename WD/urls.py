"""
URL configuration for WD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from diaryapp import views


#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('write/', views.write_diary, name='write_diary'),
#    path('read/', views.read_diary, name='read_diary'),
#    path('', views.read_diary)
#]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.instructions, name='home'),
#     path('select/', views.select_table, name='select_table'),
#     path('write/', views.write_diary, name='write_diary'),
#     path('read/', views.read_diary, name='read_diary'),
# ]

urlpatterns = [
    path('', views.instructions, name='home'),
    path('start-task/', views.start_task, name='start_task'), # Not defined yet
    path('task-in-progress/', views.task_in_progress, name='task_in_progress'),
    path('done-with-task/', views.done_with_task, name='done_with_task'),
    path('finish-task/', views.finish_task, name='finish_task'), # NOt defined yet
    path('read/', views.read_diary, name='read_diary'),
]