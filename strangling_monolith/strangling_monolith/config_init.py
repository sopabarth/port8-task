from redis import Redis
import json
import logging
import os

logger = logging.getLogger('django')


def load_routing_rules():
    logger.info('Loading routing rules...')

    redis = Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))

    with open("routing_rules.json", "r") as file:
        rules = json.load(file)

    for key, value in rules.items():
        redis.set(name=key, value=value)
