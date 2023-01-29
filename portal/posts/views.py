import time

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django_filters.views import FilterView

from core.decorators import adminuser_required
from posts.filters import AdminPostFilter, PostFilter
from posts.forms import AdminPostCategoryForm, PostEditForm, PostSearchForm
from posts.models import Post, PostCategory
from users.models import Group


class PostListView(LoginRequiredMixin, FilterView):
    model = Post
    template_name = 'posts/post_list.html'
    paginate_by = 10
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = Post.objects.select_related('category').filter(
            is_published=True, is_for_deleting=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostSearchForm(self.request.GET or None)
        context['search_form'] = form
        return context


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostEditForm(data=request.POST or None,
                            instance=post)
        if form.is_valid():
            data = {'message': 'success update'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = PostEditForm(instance=post)
    latest_posts = Post.objects.all().order_by('-created_at')[:10]
    context = {'post': post,
               'form': form,
               'latest_posts': latest_posts}
    return render(request, 'posts/post_detail.html', context=context)


class AdminPostListView(FilterView):
    model = Post
    template_name = 'posts/admin_post_list.html'
    paginate_by = 10
    filterset_class = AdminPostFilter

    def get_queryset(self):
        queryset = Post.objects.select_related('category', 'author').filter(
            is_for_deleting=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostSearchForm(self.request.GET or None)
        context['search_form'] = form
        return context


@adminuser_required()
def tinymce_upload_images(request):
    image = request.FILES.getlist('file')[0]
    image_ext = image.name.split('.')[-1]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path = default_storage.save(f'post_images/image{timestr}.{image_ext}',
                                ContentFile(image.read()))
    data = {'location': settings.MEDIA_URL + path}
    return JsonResponse(data, status=200)


@adminuser_required()
def post_create(request):
    if request.method == 'POST':
        form = PostEditForm(data=request.POST or None,
                            files=request.FILES or None)
        if form.is_valid():
            data = {'message': 'success create'}
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = PostEditForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/forms/admin_post_edit_form.html',
                  context=context)


@adminuser_required()
def post_edit(request, post_id):
    post_instance = Post.objects.get(pk=post_id)
    if not post_instance:
        errors = "Не найдена запись в базе данных"
        return JsonResponse({"errors": errors}, status=404)
    if request.method == 'POST':
        form = PostEditForm(data=request.POST or None,
                            files=request.FILES or None,
                            instance=post_instance)
        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.author = request.user
            post_instance.save()
            post_instance.groups.clear()
            groups = Group.objects.filter(
                title__in=form.data.getlist('groups'))
            post_instance.groups.set(groups)
            data = {'message': 'success editing'}
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = PostEditForm(instance=post_instance)
    context = {
        'form': form,
    }
    return render(request, 'posts/forms/admin_post_edit_form.html',
                  context=context)


@adminuser_required()
def post_remove(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"errors": 'document does not exist'},
                            status=400)
    post.is_for_deleting = True
    post.save()
    data = {'message': 'success removing'}
    return JsonResponse(data, status=200)


class AdminPostCategoryView(ListView):
    paginate_by = 10
    template_name = 'posts/admin_postcategory_list.html'
    queryset = PostCategory.objects.all()


@adminuser_required()
def category_create(request):
    if request.method == 'POST':
        form = AdminPostCategoryForm(data=request.POST or None)
        if form.is_valid():
            data = {'message': 'success create'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = AdminPostCategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/forms/admin_postcategory_form.html',
                  context=context)


@adminuser_required()
def category_edit(request, slug):
    cat_instance = get_object_or_404(PostCategory, slug=slug)
    if request.method == 'POST':
        form = AdminPostCategoryForm(data=request.POST or None,
                                     instance=cat_instance)
        if form.is_valid():
            data = {'message': 'success update'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = AdminPostCategoryForm(instance=cat_instance)
    context = {
        'form': form,
    }
    return render(request, 'posts/forms/admin_postcategory_form.html',
                  context=context)


@adminuser_required
def category_remove(request, slug):
    if request.method == 'POST':
        try:
            cat = PostCategory.objects.get(slug=slug)
        except PostCategory.DoesNotExist:
            return JsonResponse({"errors": 'Рубрика не существует'},
                                status=400)
        cat.delete()
        data = {'message': 'success removing'}
        return JsonResponse(data, status=200)
