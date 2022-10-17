from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import render

from authapp.forms import CustomPasswordChangeForm
from .forms import UserProfileForm, UserForm
from .models import Profile
from .utils import image_fetcher

User = get_user_model()

account_activation_token = default_token_generator

def user_list(request):
    pass

def user_profile(request, user_id):
    print(request)
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


def remove_avatar(request):
    if request.method == 'POST':
        # profile = Profile(user=request.user)
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
