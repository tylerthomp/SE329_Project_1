import requests
import os
import json

from models import Photo

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
        obj = json.loads(r.content)
        p = Photo(uid=obj['img_uid'])
        p.save()
        return r

    """ Takes a uid returned in upload_image()'s response and gives you info about the photo. """
    def get_image_info(self, uid):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'img_uid': uid}
        return requests.post(self.base_url() + 'GetImageInfo', post_data)

    def send_recognition_request(self, photo_uid, face_uids):
        uid_str = ''
        for uid in face_uids:
            uid_str += uid + ','

        # Below code clears out extra comma at end of string
        uid_str[-1] = ''
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'targets': photo_uid,
                     'faces_uids': uid_str}

        return requests.post(self.base_url() + 'RecognizeFaces')

    def add_new_person(self, face_info, related_img_uid):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'face_info': face_info,
                     "img_uid": related_img_uid}
        return requests.post(self.base_url() + 'FaceInfo_New', post_data)

    def set_person_name(self, face_uid, name_str):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'faces_uids': face_uid,
                     'person_id': name_str}
        return requests.post(self.base_url() + 'SetPerson', post_data)

