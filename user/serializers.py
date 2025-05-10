from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from admin_app.models import *

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self,data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')
        
        if user.category != 'user':
            raise serializers.ValidationError('Your are not an user to login')
    
        if not check_password(password,user.password):
            raise serializers.ValidationError('Password is not correct')
    
        data['user'] = user
        return data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date']
        
class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'hours']

    def validate(self, data):
        status = data.get('status')
        completion_report = data.get('completion_report')
        hours = data.get('hours')

        if status == 'Completed':
            if not completion_report:
                raise serializers.ValidationError({
                    'completion_report': 'This field is required when marking task as Completed.'
                })
            if not hours:
                raise serializers.ValidationError({
                    'hours': 'This field is required when marking task as Completed.'
                })
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completion_report', 'hours']