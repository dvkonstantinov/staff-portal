from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django_filters.views import FilterView

from authapp.forms import CustomPasswordChangeForm
from .filters import UserFilter
from .forms import UserProfileForm, UserForm, UserSearchForm
from .models import Profile
from .utils import image_fetcher

User = get_user_model()

account_activation_token = default_token_generator

USERS_PER_PAGE = 5


class UserListView(FilterView):
    model = User
    template_name = 'users/user_list.html'
    paginate_by = USERS_PER_PAGE
    filterset_class = UserFilter
    queryset = User.objects.filter(is_active=True, verified=True)
    # def get_queryset(self):
    #     filter_val = self.request.GET.get('filter', 'give-default-value')
    #     order = self.request.GET.get('orderby', 'give-default-value')
    #     new_context = Update.objects.filter(
    #         state=filter_val,
    #     ).order_by(order)
    #     return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserSearchForm(self.request.GET or None)
        context['user_search_form'] = form
        print(context)
        # context['filter'] = self.request.GET.get('filter',
        #                                          'give-default-value')
        # context['orderby'] = self.request.GET.get('orderby',
        #                                           'give-default-value')
        return context
# @login_required
# def user_list(request):
#     # users = User.objects.filter(is_active=True, verified=True)
#
#     # paginator = Paginator(users, USERS_PER_PAGE)
#     # page_number = request.GET.get('page')
#     # page_obj = paginator.get_page(page_number)
#     # context = {
#     #     'page_obj': page_obj
#     # }
#     qs = User.objects.all()
#     print(request.GET)
#     f = UserFilter(data=request.GET, queryset=qs)
#     print(f.queryset)
#     # name_contains_query = request.GET.get('name')
#
#     # if name_contains_query != '' and name_contains_query is not None:
#     #     qs = qs.filter(first_name__icontains=name_contains_query)
#     # print(qs)
#     context = {
#         'page_obj': qs
#     }
#     return render(request, 'users/user_list.html', context=context)


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
        print(default_photo)
        print(default_thumb)
        profile = Profile.objects.get(user=request.user)
        profile.photo = default_photo
        profile.thumbnail = default_thumb
        profile.save()
        return JsonResponse({'message': 'success'}, status=200)
    else:
        return JsonResponse({'errors': 'method not allowed'}, status=400)
