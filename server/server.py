
from collections import defaultdict
from queue import Queue, Empty
import json
import uuid

from flask import Flask, jsonify, request, Response

app = Flask(__name__)
cameras = defaultdict(Queue)
requests = defaultdict(Queue)

@app.route('/camera/accept/<camera_id>', methods=['GET'])
def camera_accept(camera_id):
    try:
        return cameras[camera_id].get(timeout=10)
    except Empty:
        return '', 204

@app.route('/camera/response/<camera_id>/<request_id>', methods=['PUT'])
def camera_response(camera_id, request_id):
    requests[request_id].put(request.get_data())
    del requests[request_id]
    return '', 204

@app.route('/app/request/<camera_id>', methods=['GET'])
def app_request(camera_id):
    request_id = str(uuid.uuid4())
    cameras[camera_id].put(Response(
        json.dumps(
            {
                'args': dict(request.args),
                'requestId': request_id
            }))
    )
    try:
        return Response(requests[request_id].get(timeout=10))
    except Empty:
        return '', 502
