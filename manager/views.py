from django.shortcuts import render, redirect, get_object_or_404
from admin_app.models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# Create your views here.

def manager_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            manager = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request,'Invalid email or password')
            return redirect('manager:manager_login')
        if manager.category != 'Admin':
            messages.error(request,'Access denied, you are not an admin')
            return redirect('manager:manager_login')

        if check_password(password,manager.password):
            request.session['manager_id'] = manager.id
            request.session['manager_username'] = manager.username
            messages.success(request,'Welcome')
            return redirect('manager:manager_index')
        else:
            messages.error(request,'Invalid email or password')
            return redirect('manager:manager_login')

    return render(request,'auth/manager_login.html')

def manager_signout(request):
    request.session.flush()
    messages.success(request,'Successfylly logged out')
    return redirect('manager:manager_login')

def manager_index(request):
    task_count = Task.objects.count()
    return render(request,'manager_index.html',{'task_count': task_count})

def manager_list_task(request):
    tasks = Task.objects.all().order_by('-id')
    users = CustomUser.objects.filter(category='user')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')

        if Task.objects.filter(title=title).exists():
            messages.error(request,'This title already exists')
            return redirect('manager:manager_list_task')

        assigned_to = get_object_or_404(CustomUser, id=assigned_to_id)

        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date)
        messages.success(request,'Task added successfully')
        return redirect('manager:manager_list_task')

    return render(request,'Task/list_task.html',{'tasks': tasks, 'users': users})

def manager_edit_task(request,task_id):
    tasks = get_object_or_404(Task, id=task_id)
    users = CustomUser.objects.filter(category='user')

    if request.method == 'POST':
        tasks.title = request.POST.get('title')
        tasks.description = request.POST.get('description')
        tasks.assigned_to_id = request.POST.get('assigned_to')
        tasks.due_date = request.POST.get('due_date')
        tasks.save()
        messages.success(request,'Task updated successfully')
        return redirect('manager:manager_list_task')

    return render(request,'Task/list_task.html',{'tasks': tasks, 'users': users})

def manager_delete_task(request,task_id):
    tasks = get_object_or_404(Task, id=task_id)
    tasks.delete()
    messages.success(request,'Task deleted successfully')
    return redirect('manager:manager_list_task')


