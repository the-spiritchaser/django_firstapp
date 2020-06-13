from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    params = {
        'title':'Hello/Index',
        'msg':'サンプルページです',
        'goto':'next',
    }
    return render(request, 'hello/index.html', params)

def next(request):
    params = {
            'title':'Hello/Next',
            'msg':'これは、もう１つのページです。',
            'goto':'index',
        }
    return render(request, 'hello/index.html', params)
