from flask import Flask, request, jsonify
from requests import get
import re
import json
from datetime import datetime
import redis
import os
redis_instance = redis.from_url(os.environ.get("REDIS_URL"))
app = Flask(__name__)


@app.route('/')
def hello():
    return 'fuck off'


@app.route("/post/<int:post_id>")
def get_availability(post_id):
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    num_guests = request.args.get('num_guests', 1)
    available = True
    check_results = dict()
    for name, func in CHECKS.iteritems():
        resp = func(post_id)
        if not json.loads(resp.data)['available']:
            available = False
        check_results[name] = available
    return jsonify(
        checkInDate=start_date,
        checkOutDate=end_date,
        available=available,
        numOfGuests=num_guests,
        **check_results
    )


@app.route("/post/<int:post_id>/vrbo", methods=['GET'])
def get_vrbo_availablility(post_id):
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    num_guests = request.args.get('num_guests', 1)
    vrbo_id = _get_vrbo_id(post_id)
    resp = _get_vrbo_dates(vrbo_id, start_date, end_date, num_guests)
    return jsonify(
        checkInDate=start_date,
        checkOutDate=end_date,
        available=resp,
        numOfGuests=num_guests
    )


@app.route("/post/<int:post_id>/airbnb", methods=['GET'])
def get_airbnb_availablility(post_id):
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    num_guests = request.args.get('num_guests', 1)
    airbnb_id = _get_airbnb_id(post_id)
    resp = _get_airbnb_dates(airbnb_id, start_date, end_date, num_guests)
    return jsonify(
        checkInDate=start_date,
        checkOutDate=end_date,
        available=resp,
        numOfGuests=num_guests
    )

CHECKS = dict(
    siteVrbo=get_vrbo_availablility,
    siteAirbnb=get_airbnb_availablility
)


def _get_vrbo_id(post_id):
    return 721736


def _get_airbnb_id(post_id):
    return 6591108


def _get_airbnb_dates(airbnb_id, start_date, end_date, num_of_guests):
    params = [
        ('checkin', start_date),
        ('checkout', end_date),
        ('number_of_guests', num_of_guests),
        ('hosting_id', airbnb_id)
    ]
    url = 'https://www.airbnb.com/rooms/ajax_refresh_subtotal'
    r = get(url, params=params)
    return r.json()['available']


def _get_vrbo_dates(vrbo_id, start_date, end_date, num_of_guests):
    date_format = '%m/%d/%Y'
    vrbo_url = 'https://www.vrbo.com/%s' % vrbo_id
    r = get(vrbo_url)
    if r.status_code == 200:
        m = re.search('VRBO.unitAvailability = ({.+})', r.text)
    o = json.loads(m.group(1))
    date_range = o['dateRange']
    date_start = date_range['beginDate']
    datetime_start = datetime.strptime(date_start, date_format)
    check_in_date = datetime.strptime(start_date, date_format)
    check_out_date = datetime.strptime(end_date, date_format)

    delta = (check_in_date - datetime_start).days

    check_range_delta = (check_out_date - check_in_date).days
    availability_str = o['unitAvailabilityConfiguration']['availability']
    for x in range(delta, delta+check_range_delta):
        if availability_str[x] == 'N':
            return False
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0')
