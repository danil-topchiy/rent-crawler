from marshmallow import Schema, fields


class RentObjectSchema(Schema):
    id = fields.Function(func=lambda x: str(x.id))
    parsed_date = fields.Str(dump_to='parsedDate')
    published_date = fields.Str(dump_to='publishedDate')
    city_district_title = fields.Function(func=lambda x: x.city_district.title, dump_to='cityDistrictTitle')
    short_title = fields.Str(dump_to='shortTitle')

    class Meta:
        fields = ['title', 'text', 'parsed_date', 'published_date', 'rooms', 'price', 'url', 'city_district_title',
                  'id', 'short_title']


class CityDistrictSchema(Schema):
    id = fields.Function(func=lambda x: str(x.id))

    class Meta:
        fields = ['id', 'title']


rent_objects_schema = RentObjectSchema(many=True)
city_districts_schema = CityDistrictSchema(many=True)
