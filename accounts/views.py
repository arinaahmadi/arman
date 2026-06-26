from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from accounts.forms import GroupForm, UserForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission




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
                else:
                    return redirect('accounts:login')

        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def users_view(request):
    users = User.objects.all()
    groups = Group.objects.all()

    context = {'users':users,'groups':groups}
    return render(request,'accounts/users.html',context)

def edit_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:users')   # یا هر صفحه‌ای که می‌خواهی
    else:
        form = UserForm(instance=user)

    return render(request, 'accounts/edituser.html', {'user_id':user_id,'form': form})

def new_group_view(request):

    # models_list = ContentType.objects.all().order_by('app_label', 'model')

    content_types = ContentType.objects.exclude(
        app_label__in=['admin', 'auth', 'contenttypes', 'sessions']
    ).order_by('app_label', 'model')

    models_list = []
    for ct in content_types:
        model_class = ct.model_class()
        if model_class:
            models_list.append({
                'id': ct.id,
                'app_label': ct.app_label,
                'model': ct.model,
                'model_name': model_class.__name__,
            })


    
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            # selected_permissions = []

            for item in models_list:
                ct_id = item['id']
                model_name = item['model']

                if f'perm_{ct_id}_view' in request.POST:
                    permission = Permission.objects.filter(
                        content_type_id=ct_id,
                        codename=f'view_{model_name}'
                    ).first()
                    if permission:
                        group.permissions.add(permission)

                if f'perm_{ct_id}_add' in request.POST:
                    permission = Permission.objects.filter(
                        content_type_id=ct_id,
                        codename=f'add_{model_name}'
                    ).first()
                    if permission:
                        group.permissions.add(permission)

                if f'perm_{ct_id}_change' in request.POST:
                    permission = Permission.objects.filter(
                        content_type_id=ct_id,
                        codename=f'change_{model_name}'
                    ).first()
                    if permission:
                        group.permissions.add(permission)

                if f'perm_{ct_id}_delete' in request.POST:
                    permission = Permission.objects.filter(
                        content_type_id=ct_id,
                        codename=f'delete_{model_name}'
                    ).first()
                    if permission:
                        group.permissions.add(permission)


            # selected_permissions = []

            # for item in models_list:
            #     ct_id = item['id']

            #     permissions_data = {
            #         'content_type_id': ct_id,
            #         'app_label': item['app_label'],
            #         'model': item['model'],
            #         'model_name': item['model_name'],
            #         'view': f'perm_{ct_id}_view' in request.POST,
            #         'add': f'perm_{ct_id}_add' in request.POST,
            #         'change': f'perm_{ct_id}_change' in request.POST,
            #         'delete': f'perm_{ct_id}_delete' in request.POST,
            #     }

            #     if (
            #         permissions_data['view'] or
            #         permissions_data['add'] or
            #         permissions_data['change'] or
            #         permissions_data['delete']
            #     ):
            #         selected_permissions.append(permissions_data)

            # print("selected_permissions =", selected_permissions)
            # form.save()
            return redirect('accounts:users')  # نام url صفحه‌ای که لیست گروه‌ها/کاربرها را نشان می‌دهد
    else:
        form = GroupForm()

    return render(request, 'accounts/newgroup.html', {
        'form': form,
        'models_list': models_list,
        })



@login_required
@permission_required('auth.add_user', raise_exception=True)
def new_user_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print("cleaned_data =", form.cleaned_data)
            form.save()
            return redirect('accounts:users')  # نام url صفحه‌ای که لیست گروه‌ها/کاربرها را نشان می‌دهد
        else:
            print("start")
            print(form.errors)   # برای دیباگ
            print("end")
    else:
        form = UserForm()

    return render(request, 'accounts/newuser.html', {'form': form})


def edit_group_view(request, group_id):

    group = get_object_or_404(Group, id=group_id)

    content_types = ContentType.objects.exclude(
        app_label__in=['admin', 'contenttypes', 'sessions']
    ).order_by('app_label', 'model')

    actions = ['view', 'add', 'change', 'delete']

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            group = form.save()
            permissions_to_set = []

            for ct in content_types:
                model_class = ct.model_class()
                if not model_class:
                    continue

                for action in actions:
                    checkbox_name = f'perm_{ct.id}_{action}'

                    if checkbox_name in request.POST:
                        permission = Permission.objects.filter(
                            content_type=ct,
                            codename=f'{action}_{ct.model}'
                        ).first()

                        if permission:
                            permissions_to_set.append(permission)

            group.permissions.set(permissions_to_set)

            return redirect('accounts:users')
    else:
        form = GroupForm(instance=group)

    group_permissions = group.permissions.values_list('content_type_id', 'codename')

    selected_permissions = {
        f'{content_type_id}_{codename}'
        for content_type_id, codename in group_permissions
    }

    models_list = []

    for ct in content_types:
        model_class = ct.model_class()
        if not model_class:
            continue

        models_list.append({
            'id': ct.id,
            'app_label': ct.app_label,
            'model': ct.model,
            'model_name': model_class.__name__,
            'can_view': f'{ct.id}_view_{ct.model}' in selected_permissions,
            'can_add': f'{ct.id}_add_{ct.model}' in selected_permissions,
            'can_change': f'{ct.id}_change_{ct.model}' in selected_permissions,
            'can_delete': f'{ct.id}_delete_{ct.model}' in selected_permissions,
        })

    return render(request, 'accounts/editgroup.html', {
        'form': form,
        'group': group,
        'models_list': models_list,
    })