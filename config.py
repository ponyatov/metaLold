import os, sys

try:
    ENV_IP = os.environ['IPz']
except KeyError:
    ENV_IP = '127.0.0.1'

try:
    ENV_PORT = os.environ['PORT']
except KeyError:
    ENV_PORT = 19999

HTTP_IP = ENV_IP
HTTP_PORT = ENV_PORT

REDIS_IP = ENV_IP
REDIS_PORT = 6379
