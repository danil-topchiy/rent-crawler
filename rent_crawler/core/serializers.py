from marshmallow import Schema, fields


class RentObjectSchema(Schema):
    parsed_date = fields.Str(dump_to='parsedDate')
    published_date = fields.Str(dump_to='publishedDate')
    city_district_title = fields.Function(func=lambda x: x.city_district.title, dump_to='cityDistrictTitle')

    class Meta:
        fields = ['title', 'text', 'parsed_date', 'published_date', 'rooms', 'price', 'url', 'city_district_title']


rent_objects_schema = RentObjectSchema(many=True)
