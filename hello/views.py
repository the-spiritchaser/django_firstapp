from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    params = {
        'title':'Hello/Index',
        'msg':'サンプルページです',
    }
    return render(request, 'hello/index.html', params)
