from rent_crawler.core.models import RentObject


class MongoDbPipeline(object):

    def process_item(self, item, spider):
        rent_object = RentObject(**item)
        rent_object.save()
        return item
