import sqlite3

from eyewitness.detection_utils import DetectionResultHandler
from eyewitness.models import detection_models
from peewee import SqliteDatabase


class BboxNativeSQLiteDbWriter(DetectionResultHandler):
    def __init__(self, db_path):
        """
        Parameters:
        -----------
        db_path: str
            database path
        """
        self.conn = sqlite3.connect(db_path)
        self.create_db_table()

    def handle(self, detection_result):
        """
        handle detection result

        Parameters:
        -----------
        detection_result: DetectionResult
            detection result
        """
        image_id = detection_result.image_id
        self.insert_detection_objs(
            image_id, detection_result.detected_objects)

    def create_db_table(self):
        """
        create table in the db file in db if table not exist
        """
        print('connet/create image_info table')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS ImageInfo(
                          image_id TEXT PRIMARY KEY,
                          timestamp TIMESTAMP
                          )''')

        print('connet/create bbox_detection_results table')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS BboxDetectionResult(
                          ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          image_id TEXT,
                          x1 INTEGER,
                          y1 INTEGER,
                          x2 INTEGER,
                          y2 INTEGER,
                          label TEXT,
                          score REAL,
                          meta TEXT,
                          FOREIGN KEY(image_id) REFERENCES image_info(image_id)
                          )''')
        self.conn.commit()

    def insert_image_info(self, image_id, arrive_timestamp):
        """
        insert image_info which used for unit-test

        Parameters:
        -----------
        image_id: str
            image_id
        arrive_timestamp: datetime.datetime
            the timestamp image arrive
        """
        try:
            self.conn.execute('''INSERT INTO ImageInfo(image_id, timestamp)
                              VALUES(?,?)''', (image_id, arrive_timestamp))
            self.conn.commit()
        except Exception:
            pass

    def insert_detection_objs(self, image_id, detected_objects):
        """
        insert detection results into db.

        Parameters:
        -----------
        image_id: str
            image_id
        detected_objects: List[BoundedBoxObject]
            detected objects
        """
        try:
            for detected_obj in detected_objects:
                left, top, right, bottom, class_name, score, meta = detected_obj
                self.conn.execute(
                    '''INSERT INTO BboxDetectionResult
                       (image_id, x1, y1, x2, y2, label, score, meta)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (image_id, left, top, right, bottom, class_name, score, meta))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass


class BboxPeeweeSQLiteDbWriter(DetectionResultHandler):
    def __init__(self, db_path):
        """
        Parameters:
        -----------
        db_path: str
            database path
        """
        # setup database for models
        self.database = SqliteDatabase(db_path)
        detection_models.DataBase_PROXY.initialize(self.database)
        self.create_db_table()

    def check_proxy_db(self):
        if not (self.database is detection_models.DataBase_PROXY.obj):
            detection_models.DataBase_PROXY.initialize(self.database)

    def handle(self, detection_result):
        """
        Parameters:
        -----------
        detection_result: DetectionResult
            detection_result
        """
        image_id = detection_result.image_id
        self.insert_detection_objs(
            image_id, detection_result.detected_objects)

    def create_db_table(self):
        """
        create table in the db file in db if table not exist
        """
        detection_models.ImageInfo.create_table()
        detection_models.BboxDetectionResult.create_table()

    def insert_image_info(self, image_id, arrive_timestamp):
        """
        insert image_info which used for unit-test

        Parameters:
        -----------
        image_id: str
            image_id
        arrive_timestamp: datetime.datetime
            the timestamp image arrive
        """
        try:
            self.check_proxy_db()
            image_info = detection_models.ImageInfo(image_id=image_id, timestamp=arrive_timestamp)
            # according to document:
            # http://docs.peewee-orm.com/en/latest/peewee/models.html#non-integer-primary-keys-composite-keys-and-other-tricks
            # model with Non-integer primary keys need to pass `force_insert=True`
            image_info.save(force_insert=True)
        except ValueError:
            pass

    def insert_detection_objs(self, image_id, detected_objects):
        """
        insert detection results into db.

        Parameters:
        -----------
        image_id: str
            image_id
        detected_objects: List[BoundedBoxObject]
            detected objects
        """
        try:
            self.check_proxy_db()
            for detected_obj in detected_objects:
                left, top, right, bottom, class_name, score, meta = detected_obj
                detection_result = detection_models.BboxDetectionResult(
                    image_id=image_id, x1=left, y1=top, x2=right, y2=bottom, label=class_name,
                    score=score, meta=meta)
                detection_result.save()
        except ValueError:
            pass
