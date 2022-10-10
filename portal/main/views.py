from http import HTTPStatus

from django.shortcuts import render


def qwe(request):
    return render(request, 'main/main.html')
