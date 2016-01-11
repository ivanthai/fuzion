from flask import Flask
import redis as Redis
import os

app = Flask(__name__)
redis = Redis.from_url(os.environ.get("REDIS_URL"))
from app import views

from os import path
accounts_dir = path.join(
    path.dirname(path.realpath(__file__)), '../accounts.txt'
)
with file(accounts_dir, 'r') as accounts_file:
    for line in accounts_file.readlines():
        print line
        id, v_id, a_id = line.split(',')
        redis.rpush('listings', 'listings:'+id)
        redis.hset('listings:'+id, 'airbnb', a_id)
        redis.hset('listings:'+id, 'vrbo', v_id)
