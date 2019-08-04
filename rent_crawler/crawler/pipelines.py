from rent_crawler.core.models import RentObject, CityDistrict

from mongoengine.errors import DoesNotExist


class MongoDbPipeline(object):

    def process_item(self, item, spider):
        rent_object = RentObject(**{key: item.get(key) for key in RentObject._fields.keys()})
        city_district_title = item.get('city_district_title')
        if city_district_title:
            try:
                city_district = CityDistrict.objects.get(title=city_district_title)
            except DoesNotExist:
                city_district = CityDistrict.objects.create(title=city_district_title)
            rent_object.city_district = city_district
        rent_object.save()
        return item
