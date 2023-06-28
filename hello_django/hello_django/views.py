from django.http import HttpResponse


def hello():
    return HttpResponse('hello world')
