import requests
import os
import json

from models import Person

class BetaFaceApiWrapper:
    def __init__(self):
        return

    def base_url(self):
        return 'http://www.betafaceapi.com/service_json.svc/'

    def api_key(self):
        return 'd45fd466-51e2-4701-8da8-04351c872236'

    def api_secret(self):
        return '171e8465-f548-401d-b63b-caf0dc28df5f'

    """ Takes a photo path relative to /SE321_Project_1/face_upload directory and returns an HttpResponse object. """
    def upload_image(self, relative_photo_path):
        project_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        location = project_dir + "/" + relative_photo_path
        with open(location, "rb") as image_file:
            encoded_string = image_file.read().encode("base64")
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'imagefile_data': encoded_string,
                     'original_filename': relative_photo_path}

        r = requests.post(self.base_url() + 'UploadNewImage_File', post_data)
        return r

    """ Takes a uid returned in upload_image()'s response and gives you info about the photo.
        Also takes the name of the person and attaches it to their face ID. """
    def get_image_info(self, uid, name):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'img_uid': uid}

        r = requests.post(self.base_url() + 'GetImageInfo', post_data)
        json_obj = json.loads(r.content)
        p = Person(uid=json_obj['faces'][0]['uid'], name=name)
        p.save()
        return r

    """ Sends a request to match faces described in face_uids to targets in target_uids
        both uid params MUST be arrays of strings, not just strings. """
    def send_recognition_request(self, target_uids, face_uids):
        uid_str = ''
        for index in range(len(face_uids)):
            uid_str += face_uids[index]
            if index < len(face_uids) - 1:
                uid_str += ','

        t_uid_str = ''
        for index in range(len(target_uids)):
            t_uid_str += target_uids[index]
            if index < len(face_uids) - 1:
                t_uid_str += ','

        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'targets': target_uids,
                     'faces_uids': uid_str}

        return requests.post(self.base_url() + 'RecognizeFaces', post_data)

    def get_request_result(self, recognize_id):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'recognize_uid': recognize_id}
        return requests.post(self.base_url() + 'GetRecognizeResult', post_data)

    """ Don't use this. Only keeping because I worked on it a lot."""
    def add_new_person(self, face_info, related_img_uid):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'faceinfo': face_info,
                     "img_uid": related_img_uid}
        headers = {'content-type': 'application/json'}
        json_encoder = json.JSONEncoder()

        return requests.post(self.base_url() + 'FaceInfo_New', data=json_encoder.encode(post_data), headers=headers)

    """ Don't use this. Only keeping because I worked on it a lot."""
    def set_person_name(self, face_uid, name_str):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'faces_uids': face_uid,
                     'person_id': name_str}
        return requests.post(self.base_url() + 'SetPerson', post_data)
