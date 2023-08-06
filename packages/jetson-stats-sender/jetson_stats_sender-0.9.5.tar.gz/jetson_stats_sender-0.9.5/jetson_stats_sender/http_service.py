import urllib2
import json
from threading import Timer
from threading import Lock
import cv2
import base64

ENDPOINT_PATH = "/api/datareceival/datamessage"
global_http_service = None


def initialize_global_stats_sender(api_key, destination_address, camera_key=None):
    global global_http_service
    global_http_service = HttpService(api_key, destination_address, camera_key)


def initialize_global_camera_key(camera_key):
    global global_http_service
    global_http_service.set_camera_key(camera_key)


def send_per_second_stats_with_global_service(per_second_stats):
    global global_http_service
    global_http_service.send_per_second_stats(per_second_stats)


def send_per_second_stat_with_global_service(per_second_stat):
    global global_http_service
    global_http_service.send_per_second_stat(per_second_stat)


def queue_per_second_stat_for_sending_with_global_service(per_second_stat):
    global global_http_service
    global_http_service.queue_per_second_stat_for_sending(per_second_stat)


def get_global_http_service():
    global global_http_service
    return global_http_service


class HttpService:
    def __init__(self, api_key, destination_address, camera_key=None,
                 reset_max_stat_delay=3600, send_batch_delay_sec=10):
        self.api_key = api_key
        self.destination_address = destination_address
        self.camera_key = camera_key
        self.max_stat_lock = Lock()
        self.max_stat_count = 0
        self.reset_max_stat_delay_sec = reset_max_stat_delay
        self.batch_lock = Lock()
        self.per_second_stats_batch = []
        self.send_batch_delay_sec = send_batch_delay_sec
        self._initialize_scheduler()

    def send_batch(self):
        if len(self.per_second_stats_batch) > 0:
            with self.batch_lock:
                self.send_per_second_stats(self.per_second_stats_batch)
                self.per_second_stats_batch = []
        Timer(self.send_batch_delay_sec, self.send_batch, ()).start()

    def reset_max_stat_count(self):
        with self.max_stat_lock:
            self.max_stat_count = 0
        Timer(self.reset_max_stat_delay_sec, self.reset_max_stat_count, ()).start()

    def _initialize_scheduler(self):
        Timer(self.send_batch_delay_sec, self.send_batch, ()).start()
        Timer(self.reset_max_stat_delay_sec, self.reset_max_stat_count, ()).start()

    def set_camera_key(self, camera_key):
        self.camera_key = camera_key

    def queue_per_second_stat_for_sending(self, per_second_stat):
        with self.batch_lock:
            self.max_stat_lock.acquire()
            if per_second_stat.num_tracked_people > self.max_stat_count and per_second_stat.frm is not None:
                self.max_stat_count = per_second_stat.num_tracked_people
                self.max_stat_lock.release()
                retval, buf = cv2.imencode('.jpg', per_second_stat.frm)
                if retval:
                    per_second_stat.frm_jpg = base64.b64encode(buf)
                    # TODO: test what happens if you try to save frm_jpg locally
                else:
                    print "Error converting frame to .jpg image"
            else:
                self.max_stat_lock.release()
            self.per_second_stats_batch.append(per_second_stat)

    # Real implementation of the function that will send the passed in per_second_stat objects to the back-end
    # Sends multiple stats
    def send_per_second_stats(self, per_second_stats):
        url = self.get_url_for_per_second_stats_post()
        headers = self.get_headers_for_per_second_stats_post()
        json_encoded_data = self.get_json_encoded_data_for_per_second_stats(per_second_stats)
        try:
            req = urllib2.Request(url=url, data=json_encoded_data, headers=headers)
            response = urllib2.urlopen(req)
            # Right now we do nothing with the response contents,
            # but we could return what we got and compare it with what we sent
            contents = response.read()
            if 200 <= response.getcode() < 300:
                return True
            else:
                return False
        except:
            return False

    def send_per_second_stat(self, per_second_stat):
        return self.send_per_second_stats([per_second_stat, ])

    def get_url_for_per_second_stats_post(self):
        return self.destination_address + ENDPOINT_PATH

    def get_json_encoded_data_for_per_second_stats(self, per_second_stats):
        json_stats = []
        for stat in per_second_stats:
            if stat.camera_key is None or stat.camera_key == "":
                stat.camera_key = self.camera_key
            json_stats.append(stat.to_json())
        json_data = {
            "api_key": self.api_key,
            "RealTimeStats": json_stats
        }
        json_encoded_data = json.dumps(json_data)
        return json_encoded_data

    @staticmethod
    def get_headers_for_per_second_stats_post():
        return {'Content-type': 'application/json'}
