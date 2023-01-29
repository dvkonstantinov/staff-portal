import os

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django_sendfile import sendfile
from core.utils import get_last_month_objects, get_last_month_users
from docs.models import Document
from django.conf import settings
from posts.models import Post

User = get_user_model()


@login_required
def main_page(request):
    cur_user = request.user
    all_users = User.get_active_users_with_profile()
    docs = Document.get_docs_for_current_user(cur_user)
    posts = Post.get_posts_for_current_user(cur_user)
    posts_last_month = get_last_month_objects(posts)
    docs_last_month = get_last_month_objects(docs)
    users_last_month = get_last_month_users(all_users)
    unsigned_docs = docs.filter(for_signing=True).exclude(signed=request.user)
    context = {
        'posts': posts,
        'users': all_users,
        'docs': docs,
        'users_last_month': users_last_month,
        'posts_last_month': posts_last_month,
        'docs_last_month': docs_last_month,
        'unsigned_docs': unsigned_docs,
    }
    return render(request, 'main/main.html', context=context)


def protected_media(request):
    if request.user.is_authenticated:
        if settings.DEBUG:
            return sendfile(request, request.path)
        base_dir = str(settings.BASE_DIR).replace("\\", "/")
        filepath = base_dir + request.path
        response = HttpResponse("")
        response['X-Accel-Redirect'] = '/protected/' + request.path
        response['Content-Length'] = os.path.getsize(filepath)
        del response['Content-Type']
        del response['Content-Disposition']
        del response['Accept-Ranges']
        del response['Set-Cookie']
        del response['Cache-Control']
        del response['Expires']
        return response
    else:
        return HttpResponse(status=404)
