# -*- coding: UTF-8 -*-
"""
A suite of tests for the PortMapView object
"""
import unittest
from unittest.mock import patch, MagicMock

import ujson
from flask import Flask
from vlab_api_common import flask_common
from vlab_api_common.http_auth import generate_test_token


from vlab_ipam_api.lib.views import portmap


class TestPortMapView(unittest.TestCase):
    """A set of test cases for the PortMapView object"""
    @classmethod
    def setUpClass(cls):
        """Runs once for the whole test suite"""
        cls.token = generate_test_token(username='bob')

    @classmethod
    def setUp(cls):
        """Runs before every test case"""
        app = Flask(__name__)
        portmap.PortMapView.register(app)
        app.config['TESTING'] = True
        cls.app = app.test_client()
        # Mock Celery
        app.celery_app = MagicMock()
        cls.fake_task = MagicMock()
        cls.fake_task.id = 'asdf-asdf-asdf'
        app.celery_app.send_task.return_value = cls.fake_task

if __name__ == '__main__':
    unittest.main()
