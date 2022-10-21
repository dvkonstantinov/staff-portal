import base64

from django.core.files.base import ContentFile


def image_fetcher(data):
    img_format, imgstr = data.split(';base64,')
    ext = img_format.split('/')[-1]
    if ext == 'jpeg':
        ext = 'jpg'
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data
