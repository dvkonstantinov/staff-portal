from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import upper
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_http_methods
from django_filters.views import FilterView

from core.decorators import adminuser_required
from docs.filters import DocFilter
from docs.forms import DocSearchForm, AdminDocSearchForm, AdminDocEditForm, \
    AdminDocCreateForm
from docs.models import Document
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
        print(user_group)
        allowed_docs = Document.objects.filter(groups=user_group)
        print(allowed_docs)
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
        print(form.data)
        print(request.FILES)
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


@xframe_options_exempt
def doc_detail(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    extention = upper(doc.file.url.split('.')[-1])
    context = {'doc': doc,
               'extention': extention,
               'site_path': SITE_FULL_PATH}
    return render(request, 'docs/doc_detail.html', context=context)


def doc_sign(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        document = get_object_or_404(Document, id=request.POST['doc_id'])
        document.signed.add(user)
        return JsonResponse({'message': 'success sign'}, status=200)
    return JsonResponse({'errors': 'method not allowed'}, status=400)


class AdminDocListView(DocListView):
    paginate_by = 20
    template_name = 'docs/admin_doc_list.html'

    def get_queryset(self):
        return Document.objects.all()

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
        print(form.data)
        if form.is_valid():
            document = form.save()
            for group in form.data.getlist('groups'):
                group = get_object_or_404(Group, title=group)
                print(group)
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


def doc_remove(request, doc_id):
    if request.method == 'POST':
        print(doc_id)
        document = get_object_or_404(Document, id=doc_id)
        document.delete()
        return render(request, 'docs/doc_remove.html')


def category_list(request):
    pass


def category_create(request):
    pass


def category_detail(request):
    pass


def category_edit(request):
    pass


def tag_list(request):
    pass


def tag_create(request):
    pass


def tag_detail(request):
    pass


def tag_edit(request):
    pass
