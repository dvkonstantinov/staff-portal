from datetime import datetime, timezone

from django import template
from django.template.defaultfilters import upper

register = template.Library()

TIME_AGO_PHRASES = {
    'seconds': ' секунд назад',
    'minutes': ' минут назад',
    'hours': ' часов назад',
    'days': ' дней назад',
    'weeks': ' недель назад',
    'months': ' месяцев назад',
    'years': ' лет назад',
}
TIME_AGO_PHRASES_SHORT = {
    'seconds': ' сек',
    'minutes': ' мин',
    'hours': ' час',
    'days': ' дн',
    'weeks': ' нед',
    'months': ' мес',
    'years': ' г.',
}


def pretty_date(time, short=False): # noqa
    now = datetime.now(timezone.utc)
    date_phrases = TIME_AGO_PHRASES_SHORT if short else TIME_AGO_PHRASES
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 60:
            return str(second_diff) + date_phrases['seconds']
        if second_diff < 3600:
            return str(second_diff // 60) + date_phrases['minutes']
        if second_diff < 86400:
            return str(second_diff // 3600) + date_phrases['hours']
    if day_diff < 7:
        return str(day_diff) + date_phrases['days']
    if day_diff < 31:
        return str(day_diff // 7) + date_phrases['weeks']
    if day_diff < 365:
        return str(day_diff // 30) + date_phrases['months']
    return str(day_diff // 365) + date_phrases['years']


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter('fileext')
def get_file_extention(file_url):
    extention = upper(file_url.split('.')[-1])
    if not extention:
        extention = 'NONE'
    return extention


@register.filter('clearnbsp')
def clear_nbsp(text):
    return text.replace('&nbsp', '')


@register.filter('worddeclension')
def word_declension(value: int, declension_words: str):
    declension_list = list(declension_words.split(','))
    cases = [2, 0, 1, 1, 1, 2]
    if 4 < value % 100 < 20:
        idx = 2
    elif value % 10 < 5:
        idx = cases[value % 10]
    else:
        idx = cases[5]

    return str(value) + ' ' + declension_list[idx]


@register.filter('prettydate')
def get_pretty_date(date_value):
    return pretty_date(date_value, short=False)


@register.filter('prettydateshort')
def get_pretty_date_short(date_value):
    return pretty_date(date_value, short=True)
