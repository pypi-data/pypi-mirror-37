import io

import arrow
from flask import Flask
from flask import request

from eyewitness.image_id import ImageId
from eyewitness.image_utils import ImageHandler


class ObjectDetectionFlaskWrapper(object):
    def __init__(self, obj_detector, detection_result_handler):
        app = Flask(__name__)
        self.app = app
        self.obj_detector = obj_detector
        self.detection_result_handler = detection_result_handler

        @app.route("/detect_image_byte", methods=['POST'])
        def detect_image_bytes_objs():
            if 'store_image_path' not in request.headers:
                channel = request.headers['channel']
                datetime = arrow.now()
                file_format = request.headers.get('file_format', 'jpg')
                image_id = ImageId(channel, datetime, format=file_format)
            else:
                image_id = request.headers['store_image_path']

            store_raw_image = request.headers.get('store_raw', True)

            # read data from Bytes
            data = request.data
            image_data_raw = io.BytesIO(bytearray(data))
            image_raw = ImageHandler.read_image_bytes(image_data_raw)

            if store_raw_image:
                ImageHandler.save(image_raw, image_id)

            # detect objs
            detection_result = self.obj_detector.detect(image_raw, image_id)
            detection_result_handler.handle(detection_result)
            return "successfully detected"

        @app.route("/detect_image_file", methods=['POST'])
        def detect_image_file_objs():
            image_id = request.headers['image_path']
            image_raw = ImageHandler.read_image_file(image_id)
            detection_result = self.obj_detector.detect(image_raw, image_id)
            detection_result_handler.handle(detection_result)
            return "successfully detected"
