import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from redis import Redis
import json
import requests
from rest_framework.parsers import JSONParser
from .serializer import RulesSerializer

redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))


def proxy_request(request, path) -> HttpResponse:
    rule = redis.get(path).decode("utf-8")
    url = os.getenv(rule)

    if request.method == 'POST':
        response = requests.post(f'http://{url}/{path}/', data=request)
    else:
        response = requests.get(f'http://{url}/{path}/')

    django_response = HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type']
    )
    return django_response


@csrf_exempt
def add_rule(request) -> HttpResponse:
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

