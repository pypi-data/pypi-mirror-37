import urllib2
import json


ENDPOINT_PATH = "/api/datareceival/datamessage"


# Real implementation of the function that will send the passed in per_second_stat objects to the back-end
# Sends a multiple stats
def send_per_second_stats(per_second_stats):
    url = get_url_for_per_second_stats_post()
    headers = get_headers_for_per_second_stats_post()
    json_encoded_data = get_json_encoded_data_for_per_second_stats(get_api_key(), per_second_stats)
    try:
        req = urllib2.Request(url=url, data=json_encoded_data, headers=headers)
        response = urllib2.urlopen(req)
        print "Got server response after sending stat: " % response.read()
    except:
        print "send_per_second_stat failed"


def get_url_for_per_second_stats_post():
    global destination_address
    return destination_address + ENDPOINT_PATH


def get_headers_for_per_second_stats_post():
    return {'Content-type': 'application/json'}


def initialize_stats_sender(sender_api_key, sender_camera_key, sender_destination_address):
    global api_key
    api_key = sender_api_key
    global camera_key
    camera_key = sender_camera_key
    global destination_address
    destination_address = sender_destination_address


def get_api_key():
    global api_key
    return api_key


def get_camera_key():
    global camera_key
    return camera_key


def get_destination_address():
    global destination_address
    return destination_address


def get_json_encoded_data_for_per_second_stats(api_key, per_second_stats):
    global camera_key
    json_stats = []
    for stat in per_second_stats:
        stat.camera_key = camera_key
        json_stats.append(stat.to_json())
    json_data = {
        "api_key": api_key,
        "RealTimeStats": json_stats
    }
    json_encoded_data = json.dumps(json_data)
    return json_encoded_data
