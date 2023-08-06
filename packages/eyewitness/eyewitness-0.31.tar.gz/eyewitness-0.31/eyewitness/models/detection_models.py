import datetime
from peewee import (
    CharField,
    DateTimeField,
    DoubleField,
    ForeignKeyField,
    Model,
    IntegerField,
    Proxy,
)

# Using Peewee proxy to dynamically define database in runtime
# http://docs.peewee-orm.com/en/latest/peewee/database.html#dynamically-defining-a-database
DataBase_PROXY = Proxy()


class BaseModel(Model):
    class Meta:
        database = DataBase_PROXY


class ImageInfo(BaseModel):
    image_id = CharField(unique=True, primary_key=True)
    timestamp = DateTimeField(default=datetime.datetime.now)


class BboxDetectionResult(BaseModel):
    image_id = ForeignKeyField(ImageInfo, backref='tweets')
    x1 = IntegerField()
    x2 = IntegerField()
    y1 = IntegerField()
    y2 = IntegerField()
    label = CharField()
    meta = CharField()
    score = DoubleField()
