from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from accounts.forms import GroupForm



# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/') # به صفحه دلخواه هدایت کنید

        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def users_view(request):
    users = User.objects.all()
    groups = Group.objects.all()

    context = {'users':users,'groups':groups}
    return render(request,'accounts/users.html',context)


def new_group_view(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:users')  # نام url صفحه‌ای که لیست گروه‌ها/کاربرها را نشان می‌دهد
    else:
        form = GroupForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/newgroup.html', context)


def edit_group_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('accounts:users')  
    else:
        form = GroupForm(instance=group)

    context = {
        'form': form,
        'group': group
    }
    return render(request, 'accounts/editgroup.html', context)