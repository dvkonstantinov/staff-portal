from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django_sendfile import sendfile

from core.utils import get_last_month_objects, get_last_month_users
from docs.models import Document
from portal import settings
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


@login_required
def protected_media(request):
    if request.user.is_authenticated:
        base_dir = str(settings.BASE_DIR).replace("\\", "/")
        file_path = base_dir + request.path
        return sendfile(request, file_path)

    else:
        return HttpResponse(status=404)
