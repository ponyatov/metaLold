import os, sys

try:
    ENV_HOST = os.environ['HOST']
except KeyError:
    ENV_HOST = '127.0.0.1'

try:
    ENV_PORT = os.environ['PORT']
except KeyError:
    ENV_PORT = 19999

HTTP_HOST = ENV_HOST
HTTP_PORT = ENV_PORT

REDIS_HOST = ENV_HOST
REDIS_PORT = 6379
