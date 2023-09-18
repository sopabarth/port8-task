import os
from redis import Redis
from django.http import HttpResponseForbidden


class RPSLimiter:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
        max_rps = 1_000_000  # 1M RPS, change as needed
        rps_key = f"rps:{request.META['REMOTE_ADDR']}"
        rps_count = redis.incr(rps_key)
        if rps_count == 1:
            redis.expire(rps_key, 1)

        if rps_count <= max_rps:
            return self.get_response(request)
        else:
            return HttpResponseForbidden("Rate limit exceeded. Request denied.")
