# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_list_get(self):
        """Test case for list_get

        Get list of all convertes and their possible targets
        """
        headers = { 
            'Accept': 'application/xml:',
        }
        response = self.client.open(
            '/formaTAPIRest/v1/list',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_ping_get(self):
        """Test case for ping_get

        Check if server alive
        """
        headers = { 
        }
        response = self.client.open(
            '/formaTAPIRest/v1/ping',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
