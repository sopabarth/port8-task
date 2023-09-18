from django.test import TestCase, Client
from proxy_service.views import proxy_request, add_rule, redirect, health
import os
import json
import re


class ProxyTest(TestCase):
    pattern = "https?://"

    def test_health(self):
        path = "health"

        client = Client()
        request = client.get(path=path).wsgi_request

        http_response = health(request)
        self.assertEqual(http_response.status_code, 200)

    def test_redirect_legacy(self):
        path = "api/users"

        client = Client()
        request = client.get(path=path).wsgi_request

        response = redirect(request, path)
        self.assertEqual(response.status_code, 200)
        url = re.sub(self.pattern, "", response.url)
        self.assertURLEqual(url, f"{os.getenv('LEGACY')}/{path}/")

    def test_redirect_modern(self):
        path = "weblog"

        client = Client()
        request = client.get(path=path).wsgi_request

        response = redirect(request, path)
        self.assertEqual(response.status_code, 200)
        url = re.sub(self.pattern, "", response.url)
        self.assertURLEqual(url, f"{os.getenv('MODERN')}/{path}/")

    def test_redirect_not_found(self):
        path = "not_found"

        client = Client()
        request = client.get(path=path).wsgi_request

        response = redirect(request, path)
        self.assertEqual(response.status_code, 404)

    def test_proxy_request_get(self):
        path = "api/users"

        client = Client()
        request = client.get(path=path).wsgi_request

        http_response = proxy_request(request, path)
        self.assertEqual(http_response.status_code, 200)

    def test_proxy_request_post(self):
        path = "api/users"
        data = {
            "name": "morpheus",
            "job": "leader"
        }

        client = Client()
        request = client.post(path=path, data=data).wsgi_request

        http_response = proxy_request(request, path)
        self.assertEqual(http_response.status_code, 201)

    def test_add_rule(self):
        path = "add-rule"
        payload = json.dumps({
            "key": "key1",
            "value": "MODERN"
        })
        content_type = 'application/json'

        client = Client()
        request = client.post(path=path, data=payload, content_type=content_type).wsgi_request

        response = add_rule(request)
        self.assertEqual(response.status_code, 201)
