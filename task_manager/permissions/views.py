from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

User = get_user_model()

@login_required
@permission_required('accounts.can_view_profiles', '/')
def restricted_page(request):
    render(request, 'permissions/restricted_page.html', {'user': request.user})

@login_required
def su_only(request):
    if not request.user.is_superuser:
        messages.error(request, "Тільки для суперюзерів")

    render(request, 'permissions/su_page.html', {'user': request.user})


@login_required
def list_users(request):
    if not request.user.is_superuser:
        messages.error(request, "Тільки для суперюзерів")
        return redirect('home')
    
    users = User.objects.all().exclude(id=request.user.id)
    return render(request, 'permissions/user_list.html', {'users': users})

@login_required
def manage_permissions(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Тільки для суперюзерів")
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)

    content_type = ContentType.objects.get(app_label='accounts', model='customuser')
    user_model_permissions = Permission.objects.filter(content_type=content_type)

    if request.method == 'POST':
        selected_permissions = request.POST.getlist('permissions')
        user.user_permissions.set(selected_permissions)
        messages.success(request, 'Дозволи успішно надані')
        return redirect('manage_permissions', user_id=user.id)
    
    context = {
        'user': user,
        'permissions': user_model_permissions,
        'user_permissions': user.user_permissions.all()
    }
    return render(request, 'permissions/user_permissions.html', context)


def tags_page(request):
    var1, var2, var3 = None, None, None
    context = {
        'var1': var1,
        'var2': var2,
        'var3': var3,
        'text_var': 'Hello world!',
        'some_fruits': ['banana', 'apple', 'mango'],
        'fruit': 'melon'
    }
    return render(request, 'tags.html', context)
