import datetime

from rent_crawler.extensions import db


class CityDistrict(db.Document):
    title = db.StringField()

    def __str__(self):
        return "<CityDistrict: {}>".format(self.title)


class RentObject(db.Document):
    title = db.StringField()
    short_title = db.StringField()
    url = db.StringField()
    text = db.StringField()
    published_date = db.DateTimeField()
    rooms = db.IntField()
    price = db.IntField()
    city_district = db.ReferenceField(CityDistrict)

    meta = {
        "strict": False,
        # TODO: delete heavy-weight text indexes, wen search engine added
        "indexes": ['title', '$text', 'url', 'price', 'rooms', 'city_district']
    }

    def __str__(self):
        return "<RentObject: {}>".format(self.short_title)
