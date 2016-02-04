from django.shortcuts import render
from django.http import HttpResponse
from BetaFaceApiWrapper import BetaFaceApiWrapper
import json
# Create your views here.


def index(request):
    return HttpResponse(upload(request))


def upload(request):
    response_str = 'Hello World!<br><br>'
    wrapper = BetaFaceApiWrapper()

    # Second photo for comparison purposes
    rr = wrapper.upload_image('photo2.jpeg')
    jsonrr = json.loads(rr.content)
    rrr = wrapper.get_image_info(jsonrr['img_uid'], name='Chris Pratt')
    jsonrrr = json.loads(rrr.content)
    comp_face_id = jsonrrr['faces'][0]['uid']
    # End second photo code

    r = wrapper.upload_image('photo.jpg')
    response_str += 'Image Upload Response:<br>'
    response_str += r.content
    response_str += '<br><br>'
    json_ = json.loads(r.content)

    # Below Code also saves Face ID to SQLite DB with passed-in name.
    r1 = wrapper.get_image_info(json_['img_uid'], name='Chris Pratt')

    response_str += 'Image Info Response:<br>'
    response_str += r1.content
    json2_ = json.loads(r1.content)
    response_str += '<br><br>'
    encoder = json.JSONEncoder()
    response_str += 'face JSON:<br>'
    response_str += encoder.encode(json2_['faces'][0])
    response_str += '<br><br>'
    # json2_['faces'][0]['uid'] gets the unique "face" ID. Use this for all face recognition functions
    r2 = wrapper.send_recognition_request([json2_['faces'][0]['uid']], [comp_face_id])
    response_str += 'Add Person Response:<br>'
    response_str += r2.content
    json3_ = json.loads(r2.content)
    response_str += '<br><br>Recognize Result:<br>'
    r3 = wrapper.get_request_result(json3_['recognize_uid'])
    response_str += r3.content

    json3_ = json.loads(r2.content)
    while(json3_['int_response']==-1):
        response_str += '<br><br>'
        r2 = wrapper.add_new_person(json2_['faces'][0], json2_['faces'][0]['uid'])
        response_str += 'Add Person Response:<br>'
        response_str += r2.content
        json3_ = json.loads(r2.content)

    return response_str
