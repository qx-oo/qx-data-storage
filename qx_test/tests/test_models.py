import pytest
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from qx_test.star.models import ImageStar
from qx_data_storage.oss import AutoOssStorage


class TestModel:

    @pytest.mark.django_db
    def test_saveimg(self):
        img = open("qx_test/tests/test.png", 'rb').read()
        user = User.objects.create_user(
            username="test2", email='shawn@test2.com')
        ins = ImageStar.objects.create(name="test", user=user)
        ins.image.save('test_img.png', ContentFile(img), save=True)
        assert ins.image.url

    def test_autoupload(self):
        img = open("qx_test/tests/test.png", 'rb').read()
        url = AutoOssStorage().put_bytes("test_img2.png", img)
        assert url
