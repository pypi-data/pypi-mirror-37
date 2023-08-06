import os
from abc import ABCMeta, abstractmethod
from io import BytesIO
from typing import List, Optional, Union

import pkg_resources
from PIL import Image, ImageFont, ImageDraw
import numpy as np

from eyewitness.utils import make_path
from eyewitness.image_id import ImageId
from eyewitness.detection_utils import BoundedBoxObject


DEFAULT_FONT_PATH = pkg_resources.resource_filename('eyewitness', 'font/FiraMono-Medium.otf')


class ImageHandler(object):
    """
    common functions for image processing
    """
    @classmethod
    def save(cls, image: Image.Image, output_path: Union[str, ImageId]):
        if isinstance(output_path, ImageId):
            output_path = str(output_path)
        folder = os.path.dirname(output_path)
        make_path(folder)
        image.save(output_path)

    @classmethod
    def read_image_file(cls, image_path: str) -> Image.Image:
        """
        Image.open read from file
        """
        return Image.open(image_path)

    @classmethod
    def read_image_bytes(cls, image_byte: BytesIO) -> Image.Image:
        """
        Image.open support BytesIO input
        """
        return Image.open(image_byte)

    @classmethod
    def draw_bbox(
            cls,
            image: Image.Image,
            detections: List[BoundedBoxObject],
            colors: Optional[dict] = None,
            font_path: str = DEFAULT_FONT_PATH):
        if colors is None:
            colors = {}

        font = ImageFont.truetype(
            font=font_path,
            size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (image.size[0] + image.size[1]) // 300

        for (left, top, right, bottom, predicted_class, score, _) in detections:
            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)

            # creating bbox on images
            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=colors.get(predicted_class, 'red'))
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=colors.get(predicted_class, 'red'))
            draw.text(text_origin, label, fill=(0, 0, 0), font=font)


class ImageProducer(metaclass=ABCMeta):

    def __init__(self, setting: dict):
        self.setting = setting

    @abstractmethod
    def generate_img(self) -> np.array:
        pass

    @abstractmethod
    def post_img(self, image: np.array, destination: str):
        pass


def swap_channel_rgb_bgr(image: np.array):
    """
    reverse the color channel image
    convert image (w, h, c) with channel rgb -> bgr
    convert image (w, h, c) with channel bgr -> rgb
    """
    image = image[:, :, ::-1]
    return image
