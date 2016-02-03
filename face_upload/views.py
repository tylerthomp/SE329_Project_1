from django.shortcuts import render
from django.http import HttpResponse
from BetaFaceApiWrapper import BetaFaceApiWrapper
import json

# Create your views here.



def index(request):
    return HttpResponse("Hello World\n\n   " + upload(request))


def upload(request):
    wrapper = BetaFaceApiWrapper()
    r = wrapper.upload_image("photo.jpg")
    json_ = json.loads(r.content)
    r1 = wrapper.get_image_info(json_['img_uid'])
    return r.content + " " + json_['img_uid'] + " " + r1.content
