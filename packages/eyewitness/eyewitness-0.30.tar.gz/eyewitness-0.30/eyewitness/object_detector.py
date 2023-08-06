from typing import Union
from abc import ABCMeta, abstractmethod

from PIL import Image

from eyewitness.detection_utils import DetectionResult
from eyewitness.image_id import ImageId


class ObjectDetector(metaclass=ABCMeta):
    @abstractmethod
    def detect(self, image: Image, image_id: Union[str, ImageId]) -> DetectionResult:
        pass
