from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django_filters.views import FilterView

from authapp.forms import CustomPasswordChangeForm
from core.decorators import adminuser_required
from .filters import UserFilter, AdminUserFilter
from .forms import UserProfileForm, UserForm, UserSearchForm, \
    AdminGroupEditAddForm, AdminUserForm, AdminUserSearchForm
from .models import Profile, Group
from .utils import image_fetcher

User = get_user_model()

account_activation_token = default_token_generator


class UserListView(LoginRequiredMixin, FilterView):
    model = User
    template_name = 'users/user_list.html'
    paginate_by = 10
    filterset_class = UserFilter
    queryset = User.objects.select_related('profile', 'group').filter(
        is_active=True, verified=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserSearchForm(self.request.GET or None)
        context['user_search_form'] = form
        return context


@login_required
def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user_form = UserForm(request.POST or None, instance=user)
    profile_form = UserProfileForm(request.POST or None,
                                   instance=user.profile)
    password_change_form = CustomPasswordChangeForm(user=user)
    context = {
        'user': user,
    }
    if request.user.id == user_id:
        context['form'] = user_form
        context['form2'] = profile_form
        context['password_change_form'] = password_change_form

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    return render(request, 'users/user_profile.html', context=context)


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        photo_b64 = request.POST['photo']
        photo_name = request.POST['photo-name']
        thumbnail_b64 = request.POST['thumbnail']
        thumbnail_name = request.POST['thumbnail-name']
        photo = image_fetcher(photo_b64)
        thumbnail = image_fetcher(thumbnail_b64)
        user = User(id=request.user.id)
        user.profile.photo.save(photo_name, photo, save=True)
        user.profile.thumbnail.save(thumbnail_name, thumbnail, save=True)
        return JsonResponse({'message': 'success'}, status=200)
    else:
        return JsonResponse({'errors': 'method not allowed'}, status=400)


@login_required
def remove_avatar(request):
    if request.method == 'POST':
        default_photo = Profile._meta.get_field('photo').get_default()
        default_thumb = Profile._meta.get_field('thumbnail').get_default()
        profile = Profile.objects.get(user=request.user)
        profile.photo = default_photo
        profile.thumbnail = default_thumb
        profile.save()
        return JsonResponse({'message': 'success'}, status=200)
    else:
        return JsonResponse({'errors': 'method not allowed'}, status=400)


class AdminUserListView(UserListView):
    queryset = User.objects.select_related('group').filter(is_superuser=False)
    template_name = 'users/admin_user_list.html'
    filterset_class = AdminUserFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = AdminUserSearchForm(self.request.GET or None)
        context['user_search_form'] = form
        return context


@adminuser_required
def admin_user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user_form = AdminUserForm(request.POST or None, instance=user)
    profile_form = UserProfileForm(request.POST or None,
                                   instance=user.profile)
    context = {
        'user': user,
        'form': user_form,
        'form2': profile_form,
    }

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    return render(request, 'users/admin_user_profile.html',
                  context=context)


class AdminGroupListView(ListView):
    model = Group
    queryset = Group.objects.all()
    paginate_by = 10
    template_name = 'users/admin_group_list.html'


@adminuser_required
@require_http_methods(["GET", "POST"])
def admin_group_edit(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = AdminGroupEditAddForm(request.POST or None, instance=group)
        if form.is_valid():
            data = {'message': 'success'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)

    form = AdminGroupEditAddForm(instance=group)
    context = {
        'form': form,
    }
    return render(request, 'users/forms/admin_group_edit_form.html',
                  context=context)


@adminuser_required()
@require_http_methods(["GET", "POST"])
def admin_group_add(request):
    if request.method == 'POST':
        form = AdminGroupEditAddForm(request.POST or None)
        if form.is_valid():
            data = {'message': 'success'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)

    form = AdminGroupEditAddForm()
    context = {
        'form': form,
    }
    return render(request, 'users/forms/admin_group_edit_form.html',
                  context=context)


@adminuser_required
@require_http_methods(["POST"])
def admin_group_remove(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        data = {'errors': 'Группа не существует. Возможно она уже удалена '
                          'или не была создана'}
        return JsonResponse(data, status=404)
    if group.title == 'Без группы' or group.id == 1 or group.slug == 'none':
        data = {'errors': 'Нельзя удалить группу по умолчанию'}
        return JsonResponse(data, status=400)
    group.delete()
    data = {'message': 'success'}
    return JsonResponse(data, status=200)
