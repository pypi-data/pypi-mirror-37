from django.shortcuts import render
from django.http import JsonResponse
from .decorators import visit_record
from . import models
import json
# Create your views here.


@visit_record
def index(request):
    return render(request, 'ide/index.html')


@visit_record
def post_esp_ip(request):
    return JsonResponse('ok', safe=False)


def get_esp_ip(request):
    rsp = ''
    try:
        esp_ip = models.EspIP.objects.get(ip=request.META.get("REMOTE_ADDR"))
        rsp = json.dumps(dict(code=0, ip=esp_ip.get_esp_ip()))
    except:
        rsp = json.dumps(dict(code=-1, message='no record'))

    return JsonResponse(rsp, safe=False)
