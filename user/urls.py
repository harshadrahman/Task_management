from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    
   path('user/login/', UserLoginView.as_view(), name='UserLoginView'),
   path('admin/login/', AdminLoginAPIView.as_view(), name='AdminLoginAPIView'),
   
   path('get/tasks', UserTaskListApiView.as_view(), name='UserTaskListApiView'),
   path('tasks/<int:pk>/', TaskUpdateAPIView.as_view(), name='TaskUpdateAPIView'),
   path('tasks/<int:pk>/report', TaskReportAPIView.as_view(), name='TaskReportAPIView'),

]