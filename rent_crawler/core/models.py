import datetime

from rent_crawler.extensions import db


class RentObject(db.Document):
    title = db.StringField()
    short_title = db.StringField()
    url = db.StringField()
    text = db.StringField()
    parsed_date = db.DateTimeField(default=datetime.datetime.utcnow())
    published_date = db.DateTimeField()
    rooms = db.IntField()
    price = db.IntField()
