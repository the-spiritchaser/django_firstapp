from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    if 'msg' in request.GET:
        msg = request.GET['msg']
        return HttpResponse('you typed: "' + msg + '".')
    else:
        result = 'please send msg paramerer.'
    return HttpResponse(result)
