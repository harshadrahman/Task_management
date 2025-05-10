from django.urls import path
from .views import *

app_name = 'manager'

urlpatterns = [
    path('index', manager_index, name='manager_index'),
    path('', manager_login, name='manager_login'),
    path('manager/signout', manager_signout, name='manager_signout'),

    path('task/list/', manager_list_task, name='manager_list_task'),
    path('task/edit/<int:task_id>/', manager_edit_task, name='manager_edit_task'),
    path('task/delete/<int:task_id>/', manager_delete_task, name='manager_delete_task'),


]