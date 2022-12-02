from django import forms
from django.contrib.auth import get_user_model

from docs.models import Document, Category
from users.models import Group

User = get_user_model()

DOCS_SORT_CHOICES = (
    ('old', 'Сначала старые'),
    ('new', 'Сначала новые'),
)

DOCS_STATUSES = (
    ('all', 'Все'),
    ('signed', 'Подписанные'),
    ('unsigned', 'К подписанию'),
    ('to-view', 'К ознакомлению'),
)


class DocSearchForm(forms.Form):
    add_date = forms.ChoiceField(label='Дата документа',
                                 required=False,
                                 choices=DOCS_SORT_CHOICES,
                                 widget=forms.Select(
                                     attrs={'class': 'form-select',
                                            'name': 'date'}
                                 ))
    title = forms.CharField(label='Поиск по названию', required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'name': 'name'}
                            ))
    status = forms.ChoiceField(label='Статус документа',
                               required=False,
                               choices=DOCS_STATUSES,
                               widget=forms.Select(
                                   attrs={'class': 'form-select',
                                          'name': 'status'}
                               ))
    category = forms.ModelChoiceField(Category.objects.all(),
                                    label='Категория',
                                    required=False,
                                    to_field_name='title',
                                    empty_label='Все',
                                    widget=forms.Select(
                                        attrs={'class': 'form-select',
                                               'name': 'category'}
                                    ))


class AdminDocSearchForm(DocSearchForm):
    status = None


class AdminDocCreateForm(forms.ModelForm):
    title = forms.CharField(label='Название документа',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'name': 'title'}
                            ))
    description = forms.CharField(label='Краткое описание документа',
                                  widget=forms.Textarea(
                                      attrs={'class': 'form-control',
                                             'name': 'description',
                                             'rows': 5,
                                             }
                                  ))
    category = forms.ModelChoiceField(Category.objects.all(),
                                      label='Категория',
                                      to_field_name='title',
                                      empty_label=None,
                                      widget=forms.Select(
                                          attrs={'class': 'form-select',
                                                 'name': 'group'}
                                      ))
    for_signing = forms.BooleanField(label='Документ нужно подписать?',
                                     required=False,
                                     widget=forms.CheckboxInput(
                                         attrs={'class': 'form-check-input',
                                                'name': 'for_signing'}
                                     ))
    file = forms.FileField(label='Приложите файл',
                           widget=forms.ClearableFileInput(
                               attrs={'class': 'form-control',
                                      'name': 'file',
                                      'type': 'file'}
                           ))
    groups = forms.ModelMultipleChoiceField(Group.objects.all(),
                                            required=True,
                                            label='Кому доступен '
                                                  'документ',
                                            to_field_name='title',
                                            widget=forms.SelectMultiple(
                                                attrs={'id': 'multiselect',
                                                       'class': 'multiselect'}
                                            ))

    class Meta:
        model = Document
        fields = ['title', 'description', 'category', 'for_signing', 'file',
                  'groups']


class AdminDocEditForm(AdminDocCreateForm):
    def __init__(self, *args, **kwargs):
        super(AdminDocEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['groups'].initial = self.instance.groups.all()


class AdminCategoryForm(forms.ModelForm):
    title = forms.CharField(label='Название категории',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                       'name': 'title'}
                            ))
    slug = forms.SlugField(label='Slug категории',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'name': 'slug'}
                           ))
    parent = forms.ModelChoiceField(Category.objects.all(),
                                    label='Родительская категория',
                                    required=False,
                                    to_field_name='slug',
                                    empty_label='Без родителя',
                                    widget=forms.Select(
                                        attrs={'class': 'form-select',
                                               'name': 'parent'}
                                    ))

    class Meta:
        model = Category
        fields = ['title', 'slug', 'parent']