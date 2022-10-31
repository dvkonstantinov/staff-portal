from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def main_page(request):
    return render(request, 'main/main.html')
