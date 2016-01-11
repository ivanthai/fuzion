from flask import Flask, request, jsonify
from requests import get
import re
import json
from datetime import datetime
from pprint import pprint
import urllib
app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello'


@app.route("/post/<int:post_id>")
def get_availability(post_id):
    pass


@app.route("/post/<int:post_id>/vrbo", methods=['GET'])
def get_vrbo_availablility(post_id):
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    print 'dates', start_date, end_date
    vrbo_id = _get_vrbo_id(post_id)
    resp = _get_vrbo_dates(vrbo_id, start_date, end_date)
    return jsonify(
        checkInDate=start_date,
        checkOutDate=end_date,
        available=resp
    )


@app.route("/post/<int:post_id>/airbnb", methods=['GET'])
def get_airbnb_availablility(post_id):
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    print 'dates', start_date, end_date
    airbnb_id = _get_airbnb_id(post_id)
    resp = _get_airbnb_dates(airbnb_id, start_date, end_date)
    return jsonify(
        checkInDate=start_date,
        checkOutDate=end_date,
        available=resp
    )


def _get_vrbo_id(post_id):
    return 721736


def _get_airbnb_id(post_id):
    return 6591108


def _get_airbnb_dates(airbnb_id, start_date, end_date):
    params = [('checkIn', start_date), ('checkOut', end_date)]
    airbnb_url = 'https://www.airbnb.com/rooms/%s' % airbnb_id
    r = get(airbnb_url, params=params)
    # import urllib2
    # print r.url
    # content = urllib2.urlopen(r.url).read()

    print r.url
    print r.status_code
    # print r.text
    m = re.search('not available', r.text)
    print m.group(0)
    return True


def _get_vrbo_dates(vrbo_id, start_date, end_date):
    date_format = '%m/%d/%Y'
    vrbo_url = 'https://www.vrbo.com/%s' % vrbo_id
    r = get(vrbo_url)
    if r.status_code == 200:
        m = re.search('VRBO.unitAvailability = ({.+})', r.text)
    # print m.group(1)
    o = json.loads(m.group(1))
    # pprint(o)
    date_range = o['dateRange']
    date_start = date_range['beginDate']
    datetime_start = datetime.strptime(date_start, date_format)
    check_in_date = datetime.strptime(start_date, date_format)
    check_out_date = datetime.strptime(end_date, date_format)

    delta = (check_in_date - datetime_start).days

    check_range_delta = (check_out_date - check_in_date).days
    print delta, check_range_delta
    # date_end = date_range['endDate']
    availability_str = o['unitAvailabilityConfiguration']['availability']
    for x in range(delta, delta+check_range_delta):
        print availability_str[x]
        if availability_str[x] == 'N':
            return False
    # datetime_end = datetime.strptime(date_end, date_format)
    # total_delta = datetime_end - datetime_start
    # print availability_str
    # print availability_str[delta.days]
    return True

if __name__ == '__main__':
    app.run(debug=True)
