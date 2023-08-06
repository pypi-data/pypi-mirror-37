import six
from abc import ABCMeta, abstractmethod


@six.add_metaclass(ABCMeta)
class ObjectDetector():
    @abstractmethod
    def detect(self, image, image_id):
        """
        need to implement detection method which return DetectionResult obj

        Parameters
        ----------
        image: PIL.Image
            PIL.Image instance
        image_id: Union[str, ImageId]
            image_id

        Returns
        -------
        DetectionResult
        """
        pass
