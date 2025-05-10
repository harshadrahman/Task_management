from django.shortcuts import render, get_object_or_404
from admin_app.models import *
from .serializers import UserLoginSerializer, TaskSerializer, TaskUpdateSerializer, TaskReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate

# Create your views here.

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'login successfully',
                
                'token': str(refresh.access_token),
            }, status=200)
        return Response(serializer.errors, status=400)

class AdminLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.category == 'Admin':
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return Response({
                    'message':'Login successfully',
                    'token': str(access_token),
                    'refresh_token': str(refresh),
                    'role': 'Admin'
                }, status=200)

            elif user.is_superuser:
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return Response({
                    'message':'Login successfully',
                    'token': str(access_token),
                    'refresh_token': str(refresh),
                    'role': 'SuperAdmin'
                }, status=200)

            else:
                return Response({"detail": "You do not have the required role."}, status=403)
        else:
            return Response({"detail": "Invalid username or password."}, status=400)

class UserTaskListApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user).order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
class TaskUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        if task.assigned_to != request.user:
            return Response({'detail': 'You do not have permission to update this task.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user

        if user.category != 'Admin' and not user.is_superuser:
            return Response({'detail': 'Access denied. Admin and super admin only.'}, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(Task, pk=pk)

        if task.status != 'Completed':
            return Response({'detail': 'Report is only available for completed tasks.'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the report
        serializer = TaskReportSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    