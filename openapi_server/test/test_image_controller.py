# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestImageController(BaseTestCase):
    """ImageController integration test stubs"""

    @unittest.skip("image/png not supported by Connexion")
    def test_convert_image_png2_jpg(self):
        """Test case for convert_image_png2_jpg

        Convert a JPG image to PNG
        """
        body = '/path/to/file'
        headers = { 
            'Accept': 'image/jpg',
            'Content-Type': 'image/png',
        }
        response = self.client.open(
            '/v1/convert/png/to/jpg',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='image/png')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
