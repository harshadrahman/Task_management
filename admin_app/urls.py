from django.urls import path
from .views import *

app_name = 'admin_app'

urlpatterns = [
    path('', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('index', index, name='index'),

    path('list/user', list_user, name='list_user'),
    path('edit/user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete/user/<int:user_id>/', delete_user, name='delete_user'),

    path('list/admins/', list_admin, name='list_admin'),
    path('edit/admin/<int:admin_id>/', edit_admin, name='edit_admin'),
    path('delete/admin/<int:admin_id>/', delete_admin, name='delete_admin'),

    path('list/tasks', list_tasks, name='list_tasks'),
    path('task/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', delete_task, name='delete_task'),

]