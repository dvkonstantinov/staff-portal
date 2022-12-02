import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import upper
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django_filters.views import FilterView

from core.decorators import adminuser_required
from docs.filters import DocFilter
from docs.forms import DocSearchForm, AdminDocSearchForm, AdminDocEditForm, \
    AdminDocCreateForm, AdminCategoryForm
from docs.models import Document, Category
from portal.settings import SITE_FULL_PATH
from users.models import Group

DOCS_PER_PAGE = 10

User = get_user_model()


class DocListView(LoginRequiredMixin, FilterView):
    model = Document
    template_name = 'docs/doc_list.html'
    paginate_by = DOCS_PER_PAGE
    filterset_class = DocFilter

    def get_queryset(self):
        user_group = self.request.user.group
        allowed_docs = Document.objects.filter(groups=user_group,
                                               is_for_deleting=False)
        return allowed_docs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DocSearchForm(self.request.GET or None)
        context['doc_search_form'] = form
        return context


@adminuser_required()
@require_http_methods(["GET", "POST"])
def doc_create(request):
    if request.method == 'POST':
        form = AdminDocCreateForm(data=request.POST or None,
                                  files=request.FILES or None)
        if form.is_valid():
            data = {'message': 'success create'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = AdminDocCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'docs/forms/admin_doc_edit_form.html',
                  context=context)


@login_required
@xframe_options_exempt
def doc_detail(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
    except Document.DoesNotExist as err:
        return JsonResponse({"errors": err}, status=404)
    if request.user.group in doc.groups.all():
        extention = upper(doc.file.url.split('.')[-1])
        context = {'doc': doc,
                   'extention': extention,
                   'site_path': SITE_FULL_PATH}
        return render(request, 'docs/doc_detail.html', context=context)
    else:
        return HttpResponseNotFound()


@login_required
@require_http_methods(["POST"])
def doc_sign(request):
    doc_id = request.POST['doc_id']
    document = get_object_or_404(Document, id=doc_id)
    if request.user.group in document.groups.all():
        user = get_object_or_404(User, id=request.user.id)
        document.signed.add(user)
        return JsonResponse({'message': 'success sign'}, status=200)
    return JsonResponse({'errors': 'access denied'}, status=400)


class AdminDocListView(DocListView):
    paginate_by = 20
    template_name = 'docs/admin_doc_list.html'

    def get_queryset(self):
        return Document.objects.select_related('category').filter(
            is_for_deleting=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = AdminDocSearchForm(self.request.GET or None)
        context['doc_search_form'] = form
        return context


@adminuser_required
@require_http_methods(["GET", "POST"])
def doc_edit(request, doc_id):
    doc_instance = get_object_or_404(Document, pk=doc_id)
    if request.method == 'POST':
        form = AdminDocEditForm(data=request.POST or None,
                                files=request.FILES or None,
                                instance=doc_instance)
        if form.is_valid():
            document = form.save()
            for group in form.data.getlist('groups'):
                group = get_object_or_404(Group, title=group)
                document.groups.add(group.id)
            data = {'message': 'success editing'}
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = AdminDocEditForm(instance=doc_instance)
    context = {
        'form': form,
    }
    return render(request, 'docs/forms/admin_doc_edit_form.html',
                  context=context)


@adminuser_required
@require_http_methods(["POST"])
def doc_remove(request, doc_id):
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        return JsonResponse({"errors": 'document does not exist'},
                            status=400)
    document.is_for_deleting = True
    document.save()
    data = {'message': 'success removing'}
    return JsonResponse(data, status=200)


class CategoryListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'docs/category_list.html'

    def get_queryset(self):
        return Category.objects.all()


class AdminCategoryListView(CategoryListView):
    paginate_by = 10
    template_name = 'docs/admin_category_list.html'


@adminuser_required
@require_http_methods(["GET"])
def doc_signers(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    signed_users = document.signed.all()
    unsigned_users = User.objects.filter(is_superuser=False,
                                         is_active=True,
                                         verified=True,
                                         group__in=document.groups.all()
                                         ).exclude(id__in=signed_users)
    signed_users = list(signed_users.values('id', 'email', 'first_name',
                                            'last_name'))
    unsigned_users = list(unsigned_users.values('id', 'email', 'first_name',
                                                'last_name'))
    data = {'signed_users': signed_users,
            'unsigned_users': unsigned_users}
    return JsonResponse(data, status=200)


@adminuser_required
@require_http_methods(["GET", "POST"])
def category_create(request):
    if request.method == 'POST':
        form = AdminCategoryForm(data=request.POST or None)
        if form.is_valid():
            data = {'message': 'success create'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = AdminCategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'docs/forms/admin_category_form.html',
                  context=context)


def category_detail(request, slug):
    pass


@adminuser_required
@require_http_methods(["GET", "POST"])
def category_edit(request, slug):
    cat_instance = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = AdminCategoryForm(data=request.POST or None,
                                 instance=cat_instance)
        if form.is_valid():
            data = {'message': 'success update'}
            form.save()
            return JsonResponse(data, status=200)
        else:
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
    form = AdminCategoryForm(instance=cat_instance)
    context = {
        'form': form,
    }
    return render(request, 'docs/forms/admin_category_form.html',
                  context=context)


@adminuser_required
@require_http_methods(["POST"])
def category_remove(request, slug):
    if request.method == 'POST':
        try:
            cat = Category.objects.get(slug=slug)
        except Document.DoesNotExist:
            return JsonResponse({"errors": 'Категория не существует'},
                                status=400)
        try:
            cat.delete()
        except ProtectedError:
            return JsonResponse({"errors": 'В категории есть документы. '
                                           'Переназначьте категорию всем '
                                           'документам в этой категории'},
                                status=400)
        data = {'message': 'success removing'}
        return JsonResponse(data, status=200)


def tag_list(request):
    pass


def tag_create(request):
    pass


def tag_detail(request):
    pass


def tag_edit(request):
    pass
