from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
# Create your views here.



def index(request):
    return HttpResponse("Hello World   " + upload(request))

def upload(request):
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))) + '/photo.jpg'
    encoded_string = None
    with open(__location__, "rb") as image_file:
        encoded_string = image_file.read().encode("base64")

    post_data = {'api_key': 'd45fd466-51e2-4701-8da8-04351c872236',
                 'api_secret':'171e8465-f548-401d-b63b-caf0dc28df5f',
                 'imagfile_data': encoded_string,
                 'original_filename': 'photo.jpg'}
    r = requests.post('http://www.betafaceapi.com/service.svc/UploadNewImage_File', post_data)
    return r.content
