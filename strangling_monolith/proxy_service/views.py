import os

from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from prometheus_client import generate_latest
from redis import Redis
import json
import requests
import logging

from requests import Response
from rest_framework.parsers import JSONParser
from .serializer import RulesSerializer

logger = logging.getLogger('django')
redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))


def redirect(request: HttpRequest, path: str) -> Response:
    try:
        rule = redis.get(path).decode("utf-8")
        url = os.getenv(rule)
    except AttributeError as e:
        logger.error(f"Nonexistent rule for path '{path}'")
        response = Response()
        response.status_code = 404
        response.headers['Content-Type'] = 'text/plain'
        response._content = f"Nonexistent rule for path '{path}'"

        return response

    if request.method == 'GET':
        response = requests.get(url=f'https://{url}/{path}/')
    elif request.method == 'POST':
        response = requests.post(url=f'https://{url}/{path}/', data=request)
    elif request.method == 'PUT':
        response = requests.put(url=f'https://{url}/{path}/', data=request)
    elif request.method == 'PATCH':
        response = requests.patch(url=f'https://{url}/{path}/', data=request)
    elif request.method == 'DELETE':
        response = requests.delete(url=f'https://{url}/{path}/', data=request)

    return response


def proxy_request(request: HttpRequest, path: str = '/') -> HttpResponse:
    log_data = {
        'method': request.method,
        'path': request.path,
        'headers': dict(request.headers),
        'remote_addr': request.META.get('REMOTE_ADDR', ''),
    }
    logger.info(log_data)
    response = redirect(request=request, path=path)

    django_response = HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )

    return django_response


@csrf_exempt
def add_rule(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RulesSerializer(data=data)

        if serializer.is_valid():
            redis.set(name=data['key'], value=data['value'])

            with open("routing_rules.json", "r+") as file:
                rules = json.load(file)
                rules[data['key']] = data['value']
                file.seek(0)
                json.dump(rules, file)

            return HttpResponse(content=f'Path {data["key"]} with rule {data["value"]} successfully added', status=201)
        return HttpResponse(content=f'Invalid input data', status=400)


def health(request: HttpRequest) -> HttpResponse:
    logger.info('Health endpoint')
    return HttpResponse(content='Health endpoint', status=200)


def prometheus_metrics(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(content=generate_latest())
    response['Content-Type'] = 'text/plain; version=0.0.4'

    return response
