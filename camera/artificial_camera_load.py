import os
import random
import sys
from threading import Thread
import time

import requests

total_requests = 0

def printerr(msg):
    print(msg, file=sys.stderr, flush=True)

class CameraLoad:
    def __init__(self, endpoint):
        self._endpoint = endpoint
        self._total_requests = 0

    def app_loop(self, cam_id):
        while True:
            try:
                response = requests.get(
                    '%s/app/request/%d' % (self._endpoint, cam_id),
                    timeout=30)
                response.raise_for_status()
                self._total_requests += 1
            except IOError as e:
                printerr('IOError in app loop ' + str(e))
                time.sleep(random.random() * 10)

    def camera_loop(self, cam_id):
        while True:
            try:
                response = requests.get(
                    '%s/camera/accept/%d' % (self._endpoint, cam_id),
                    timeout=30)
                response.raise_for_status()
                if response.status_code == 204:
                    continue
                with open('testsrc2.mp4', 'rb') as video_file:
                    response = requests.put(
                        '%s/camera/response/%d/%s' % (
                            self._endpoint, cam_id, response.json()['requestId']),
                        data=video_file)
                    response.raise_for_status()
            except IOError as e:
                printerr('IOError in camera loop ' + str(e))
                time.sleep(random.random() * 10)

    def status_printer(self):
        while True:
            printerr(self._total_requests)
            time.sleep(5)

def main():
    endpoint = sys.argv[1]
    n_cameras = int(os.environ.get('N_CAMERAS', '1'))
    threads = []
    load = CameraLoad(endpoint)
    for i in range(n_cameras):
        threads.append(Thread(target=load.app_loop, args=(i,), daemon=True))
        threads.append(Thread(target=load.camera_loop, args=(i,), daemon=True))
    threads.append(Thread(target=load.status_printer, daemon=True))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
