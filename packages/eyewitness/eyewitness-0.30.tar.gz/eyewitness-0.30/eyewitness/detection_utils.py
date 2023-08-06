import json
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import List

from eyewitness.image_id import ImageId


BoundedBoxObject = namedtuple(
    'BoundedBoxObject', ['x1', 'y1', 'x2', 'y2', 'class_name', 'score', 'meta'])
Type_Serialization_Mapping = {'bbox': BoundedBoxObject}


class DetectionResult(object):
    """
    represent detection result of a image.
    """

    def __init__(self, image_dict, detection_type='bbox'):
        self.detection_type = Type_Serialization_Mapping[detection_type]
        if isinstance(image_dict['image_id'], ImageId):
            image_dict['image_id'] = str(image_dict['image_id'])
        self.image_dict = image_dict

    @property
    def image_id(self) -> str:
        return self.image_dict['image_id']

    @property
    def drawn_image_path(self) -> str:
        return self.image_dict.get('drawn_image_path', '')

    @property
    def detected_objects(self) -> List:
        """
        list of detected objects (will translate type into detection_type)
        """
        detected_objects = self.image_dict.get('detected_objects', [])
        return [self.detection_type(*i) for i in detected_objects]

    @classmethod
    def from_json(cls, json_str: str):
        img_dict = json.loads(json_str)
        return cls(img_dict)

    def to_json(self) -> str:
        json_str = json.dumps(self.image_dict)
        return json_str

    def to_dict(self) -> dict:
        return self.image_dict


class DetectionResultHandler(metaclass=ABCMeta):
    @abstractmethod
    def handle(self, detection_result: DetectionResult):
        pass
