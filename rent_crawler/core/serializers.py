from marshmallow import Schema, fields


class RentObjectSchema(Schema):
    parsed_date = fields.Str(dump_to='parsedDate')
    published_date = fields.Str(dump_to='publishedDate')

    class Meta:
        fields = ['title', 'text', 'parsed_date', 'published_date', 'rooms', 'price']


rent_objects_schema = RentObjectSchema(many=True)
