from django import forms

from posts.models import Post, PostCategory
from users.models import Group


class PostSearchForm(forms.ModelForm):
    content = forms.CharField(label='Поиск по новостям',
                              required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control',
                                         'name': 'content'}
                              ))
    category = forms.ModelChoiceField(PostCategory.objects.all(),
                                      label='Рубрика',
                                      to_field_name='title',
                                      empty_label='Все',
                                      required=False,
                                      widget=forms.Select(
                                          attrs={'class': 'form-select',
                                                 'name': 'category'}))

    class Meta:
        model = Post
        fields = ['content', 'category']


class PostEditForm(forms.ModelForm):
    title = forms.CharField(
        label='Название новости',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'title'}
        ))
    body = forms.CharField(
        label='Текст новости',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'name': 'description',
                   'id': 'textareaBody',
                   'rows': 5,
                   }
        ))
    category = forms.ModelChoiceField(
        PostCategory.objects.all(),
        label='Категория',
        to_field_name='title',
        empty_label=None,
        widget=forms.Select(
            attrs={'class': 'form-select',
                   'name': 'group'}
        ))
    groups = forms.ModelMultipleChoiceField(
        Group.objects.all(),
        required=True,
        label='Для каких групп новость',
        to_field_name='title',
        widget=forms.SelectMultiple(
            attrs={'id': 'multiselect',
                   'class': 'multiselect'}
        ))
    is_published = forms.BooleanField(
        label='Опубликовать новость?',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input',
                   'name': 'is_published'}
        ))

    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'groups', 'is_published']


class AdminPostCategoryForm(forms.ModelForm):
    title = forms.CharField(
        label='Название рубрики',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'title'}
        ))
    slug = forms.SlugField(
        label='Slug рубрики',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'name': 'slug'}
        ))

    class Meta:
        model = PostCategory
        fields = ['title', 'slug']
