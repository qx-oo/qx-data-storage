import pytest
import base64
import requests
import json
from django.contrib.auth.models import User
from qx_test.star.models import ImageStar


class TestView:

    def user_login(self, client):
        username = 'shawn'
        password = 'test1234'
        user = User.objects.create_user(
            username=username, email='shawn@test.com', password=password)
        client.login(username=username, password=password)
        return client, user

    @pytest.mark.django_db
    def test_model_upload(self, rf, client):
        url = '/storage/'
        img = open("qx_test/tests/test.png", 'rb').read()
        img = base64.b64encode(img).decode()

        client, user = self.user_login(client)
        i_star = ImageStar.objects.create(user=user, name='test1')

        data = {
            "type": "star_image",
            "image": img,
            "callback_params": {
                "object_id": i_star.id
            }
        }
        resp = client.post(
            url, data=data,
            content_type='application/json')
        assert resp.status_code == 200
        i_s = ImageStar.objects.get(id=i_star.id)
        assert i_s.image.url

    @pytest.mark.django_db
    def test_sign_url(self, rf, client):
        url = '/storage/upload-url/'
        data = {
            'type': 'star_image',
<<<<<<< HEAD
            'file_type': 'png',
=======
>>>>>>> fdeb60c... 添加oss授权上传图片
        }
        client, _ = self.user_login(client)
        resp = client.post(
            url, data=data,
            content_type='application/json')
        ret = json.loads(resp.content)
        upload_url = ret['data']['upload_url']
        url = ret['data']['url']
        assert url
        img = open("qx_test/tests/test.png", 'rb').read()
<<<<<<< HEAD
        headers = {
            'Content-Type': 'image/png',
        }
        resp = requests.put(upload_url, data=img, headers=headers)
=======
        resp = requests.put(upload_url, data=img)
>>>>>>> fdeb60c... 添加oss授权上传图片
        print(resp)
        assert resp.status_code == 200
