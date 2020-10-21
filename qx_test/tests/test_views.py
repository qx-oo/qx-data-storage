import pytest
import base64
from django.contrib.auth.models import User
from qx_test.star.models import ImageStar
# from qx_data_storage.viewsets import UploadImageViewset


class TestView:

    @pytest.mark.django_db
    def test_model_upload(self, rf, client):
        url = '/upload-img/'
        img = open("qx_test/tests/test.png", 'rb').read()
        img = base64.b64encode(img).decode()

        username = 'shawn'
        password = 'test1234'
        user = User.objects.create_user(
            username=username, email='shawn@test.com', password=password)
        i_star = ImageStar.objects.create(user=user, name='test1')
        client.login(username=username, password=password)

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
