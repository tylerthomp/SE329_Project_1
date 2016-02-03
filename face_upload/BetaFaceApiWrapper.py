import requests
import os


class BetaFaceApiWrapper:
    def __init__(self):
        return

    def base_url(self):
        return 'http://www.betafaceapi.com/service_json.svc/'

    def api_key(self):
        return 'd45fd466-51e2-4701-8da8-04351c872236'

    def api_secret(self):
        return '171e8465-f548-401d-b63b-caf0dc28df5f'

    def upload_image(self, relative_photo_path):
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/" + relative_photo_path
        with open(location, "rb") as image_file:
            encoded_string = image_file.read().encode("base64")
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'imagefile_data': encoded_string,
                     'original_filename': relative_photo_path}
        return requests.post(self.base_url() + 'UploadNewImage_File', post_data)

    def get_image_info(self, uid):
        post_data = {'api_key': self.api_key(),
                     'api_secret': self.api_secret(),
                     'img_uid': uid}
        return requests.post(self.base_url() + 'GetImageInfo', post_data)
