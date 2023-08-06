import json
import six
from abc import ABCMeta, abstractmethod
from collections import namedtuple

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
    def image_id(self):
        """
        Returns
        -------
        image_id: str
            image_id
        """
        return self.image_dict['image_id']

    @property
    def drawn_image_path(self):
        """
        Returns
        -------
        drawn_image_path: str
            drawn_image_path
        """
        return self.image_dict.get('drawn_image_path', '')

    @property
    def detected_objects(self):
        """
        Returns
        -------
        detected_objects: List[object]
            List of detection results
        """
        detected_objects = self.image_dict.get('detected_objects', [])
        return [self.detection_type(*i) for i in detected_objects]

    @classmethod
    def from_json(cls, json_str):
        img_dict = json.loads(json_str)
        return cls(img_dict)

    def to_json(self):
        """
        Returns
        -------
        json_str: str
            json str
        """
        json_str = json.dumps(self.image_dict)
        return json_str

    def to_dict(self):
        """
        Returns
        -------
        image_dict: dict
            the dict repsentation of detection_result
        """
        return self.image_dict


@six.add_metaclass(ABCMeta)
class DetectionResultHandler():
    @abstractmethod
    def handle(self, detection_result):
        """
        abstract method for handle DetectionResult

        Parameters:
        -----------
        detection_result: DetectionResult
        """
        pass
