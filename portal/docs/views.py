from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import upper
from django.views.decorators.clickjacking import xframe_options_exempt
from django_filters.views import FilterView

from docs.filters import DocFilter
from docs.forms import DocSearchForm
from docs.models import Document
from portal.settings import SITE_FULL_PATH

DOCS_PER_PAGE = 10

User = get_user_model()


class UserListView(LoginRequiredMixin, FilterView):
    model = Document
    template_name = 'docs/doc_list.html'
    paginate_by = DOCS_PER_PAGE
    filterset_class = DocFilter
    queryset = Document.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DocSearchForm(self.request.GET or None)
        context['doc_search_form'] = form
        return context


def doc_create(request):
    pass


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
        return JsonResponse({'message': 'success'}, status=200)
    return JsonResponse({'errors': 'method not allowed'}, status=400)


def doc_edit(request):
    pass


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
