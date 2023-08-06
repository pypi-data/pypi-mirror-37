from linebot import LineBotApi
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
    URIAction
)

from eyewitness.detection_utils import (DetectionResultHandler, DetectionResult)


class LineMessageSender(DetectionResultHandler):
    def __init__(self, audience_ids, channel_access_token, site_domain):
        """
        Parameters:
        -----------
        audience_ids: set
            line audience ids
        channel_access_token: str
            channel_access_token
        site_domain: str
            static image entry point
        """
        self.audience_ids = audience_ids
        self.line_bot_api = LineBotApi(channel_access_token)
        self.site_domain = site_domain

    def handle(self, detection_result: DetectionResult):
        # TODO : comfirm drawn_image_path
        drawn_image_path = "{}".format(str(DetectionResult))
        self.send_annotation_button_msg(drawn_image_path)

    def send_annotation_button_msg(self, img_path: str):
        """
        sent line botton msg to audience_ids

        Parameters:
        -----------
        img_path: str
            image path to be set
        """
        image_url = self.site_domain + img_path
        buttons_msg = TemplateSendMessage(
            alt_text='object detected',
            template=ButtonsTemplate(
                thumbnail_image_url=image_url,
                title='object detected',
                text='help to report result',
                actions=[
                    MessageAction(
                        label='Report Error (錯誤回報)',
                        text=img_path
                    ),
                    URIAction(
                        label='full image (完整圖片)',
                        uri=image_url
                    )
                ]
            )
        )
        self.line_bot_api.multicast(list(self.audience_ids), buttons_msg)
