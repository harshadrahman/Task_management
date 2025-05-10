from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def signin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request,'Welcome')
                return redirect('admin_app:index')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('admin_app:signin')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('admin_app:signin')
    return render(request,'auth/signin.html')

def signout(request):
    logout(request)
    return redirect('admin_app:signin')

@login_required(login_url='admin_app:signin')
def index(request):
    task_count = Task.objects.count()
    user_count = CustomUser.objects.filter(category='user').count()
    admin_count = CustomUser.objects.filter(category='Admin').count()
    
    return render(request, 'index.html',{'task_count':task_count,'user_count':user_count, 'admin_count': admin_count})

@login_required(login_url='admin_app:signin')
def list_user(request):
    users = CustomUser.objects.filter(category='user').order_by('-id')
    admins = CustomUser.objects.filter(category='Admin')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        category = request.POST.get('category')
        assigned_admin_id = request.POST.get('assigned_admin')

        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return render(request, 'user/list_user.html',{'users': users, 'admins':admins})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'user/list_user.html',{'users': users, 'admins':admins})

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "An account with this username already exists.")
            return render(request, 'user/list_user.html',{'users': users, 'admins':admins})

        hashed_password = make_password(password)

        new_user = CustomUser.objects.create(
            username=username,
            password=hashed_password,
            email=email,
            category=category
        )
        
        if category == 'user' and assigned_admin_id:
            assigned_admin = CustomUser.objects.filter(id=assigned_admin_id, category='Admin').first()
            new_user.parent_admin = assigned_admin
            new_user.save()
            
        messages.success(request, 'Data added successfully')
        return redirect('admin_app:list_user')

    return render(request,'user/list_user.html',{'users': users, 'admins': admins})

@login_required(login_url='admin_app:signin')
def edit_user(request,user_id):
    user = get_object_or_404(CustomUser,id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        category = request.POST.get('category')
        assigned_admin_id = request.POST.get('assigned_admin')


        if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request,'This email already exists')
            return render(request, 'user/list_user.html',{'user': user})

        if CustomUser.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request,'This email already exists')
            return render(request, 'user/list_user.html',{'user': user})

        if new_password or confirm_password:
            if new_password != confirm_password:
                messages.error(request,'Passwords do not match')
                return render(request, 'user/list_user.html',{'user': user})
            user.new_password = make_password(new_password)

        user.username = username
        user.email = email
        user.category = category
        if category == 'user' and assigned_admin_id:
            admin_user = CustomUser.objects.filter(id=assigned_admin_id, category='Admin').first()
            user.parent_admin = admin_user
        else:
            user.parent_admin = None
            
        user.save()
        messages.success(request,'details updated successfully')
        return redirect('admin_app:list_user')

    return render(request, 'user/list_user.html',{'user': user})

@login_required(login_url='admin_app:signin')
def delete_user(request,user_id):
    user = get_object_or_404(CustomUser,id=user_id)
    user.delete()
    messages.success(request,'User deleted successfully')
    return redirect('admin_app:list_user')

@login_required(login_url='admin_app:signin')
def list_admin(request):
    admins = CustomUser.objects.filter(category='Admin').order_by('-id')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        category = request.POST.get('category')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'admin_list/list_admin.html', {'admins': admins})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'admin_list/list_admin.html', {'admins': admins})

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "An account with this username already exists.")
            return render(request, 'admin_list/list_admin.html', {'admins': admins})

        hashed_password = make_password(password)

        CustomUser.objects.create(
            username=username,
            password=hashed_password,
            email=email,
            category=category
        )
        messages.success(request, 'Data added successfully')
        return redirect('admin_app:list_admin')
    return render(request,'admin_list/list_admin.html',{'admins': admins})

@login_required(login_url='admin_app:signin')
def edit_admin(request,admin_id):
    admin = get_object_or_404(CustomUser,id=admin_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        category = request.POST.get('category')

        if CustomUser.objects.filter(email=email).exclude(id=admin_id).exists():
            messages.error(request,'This email already exists')
            return render(request, 'admin_list/list_admin.html',{'admin': admin})

        if CustomUser.objects.filter(username=username).exclude(id=admin_id).exists():
            messages.error(request,'This username already exists')
            return render(request, 'admin_list/list_admin.html',{'admin': admin})


        if new_password or confirm_password:
            if new_password != confirm_password:
                messages.error(request,'Passwords do not match')
                return render(request, 'admin_list/list_admin.html',{'admin': admin})
            admin.new_password = make_password(new_password)

        admin.username = username
        admin.email = email
        admin.category = category
        admin.save()
        messages.success(request,'details updated successfully')
        return redirect('admin_app:list_admin')

    return render(request, 'admin_list/list_admin.html',{'admin': admin})

@login_required(login_url='admin_app:signin')
def delete_admin(request,admin_id):
    admin = get_object_or_404(CustomUser,id=admin_id)
    admin.delete()
    messages.success(request,'Data deleted successfully')
    return redirect('admin_app:list_admin')

@login_required(login_url='admin_app:signin')
def list_tasks(request):
    tasks = Task.objects.all().order_by('-id')
    users = CustomUser.objects.filter(category='user')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')

        if Task.objects.filter(title=title).exists():
            messages.error(request,'This title already exists')
            return redirect('admin_app:list_tasks')

        assigned_to = get_object_or_404(CustomUser, id=assigned_to_id)

        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date)
        messages.success(request,'Task added successfully')
        return redirect('admin_app:list_tasks')
    return render(request,'Task/task.html',{'tasks': tasks, 'users': users})

@login_required(login_url='admin_app:signin')
def edit_task(request,task_id):
    tasks = get_object_or_404(Task, id=task_id)
    users = CustomUser.objects.filter(category='user')

    if request.method == 'POST':
        tasks.title = request.POST.get('title')
        tasks.description = request.POST.get('description')
        tasks.assigned_to_id = request.POST.get('assigned_to')
        tasks.due_date = request.POST.get('due_date')
        tasks.save()
        messages.success(request,'Task updated successfully')
        return redirect('manager:list_task')

    return render(request,'Task/task.html',{'tasks': tasks, 'users': users})

@login_required(login_url='admin_app:signin')
def delete_task(request,task_id):
    tasks = get_object_or_404(Task, id=task_id)
    tasks.delete()
    messages.success(request,'Task deleted successfully')
    return redirect('manager:list_task')