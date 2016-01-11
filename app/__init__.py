from flask import Flask
import redis as Redis
import os

app = Flask(__name__)
redis = Redis.from_url(os.environ.get("REDIS_URL"))
from app import views