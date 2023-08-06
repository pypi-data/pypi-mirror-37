class ImageId(object):
    """
    the target of ImageId is used to standardize the image_id format
    default init method from pattern {chanel}_{YYYY/MM/DD/HH/mm/ss}.{fileformat}
    e.g: "channel_YYYY/MM/DD/HH/mm/ss.jpg"
    """

    def __init__(self, channel, datetime, forma='jpg', date_str_format='YYYY/MM/DD/HH/mm/ss'):
        """
        Parameters:
        -----------
        channel: str
            channel of image comes
        datetime: Arrow
            Arrow obj
        format: str
            type of image
        date_str_format: str
            date str format default is YYYY/MM/DD/HH/mm/ss
        """
        self.date_str = datetime.format(date_str_format)
        self.channel = channel
        self.format = format

    def __hash__(self):
        return hash(self.date_str) ^ hash(self.channel) ^ hash(self.format)

    def __str__(self):
        return "{}_{}.{}".format(self.channel, self.date_str, self.format)

    def __eq__(self, other):
        if isinstance(other, ImageId):
            return str(self) == str(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ImageId):
            return str(self) < str(other)
        return NotImplemented
