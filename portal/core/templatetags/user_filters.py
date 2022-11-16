from django import template
from django.template.defaultfilters import upper

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter('fileext')
def get_file_extention(file_url):
    extention = upper(file_url.split('.')[-1])
    if not extention:
        extention = 'NONE'
    return extention
