from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, World<br><a href='./finance'>Finance</a>")
