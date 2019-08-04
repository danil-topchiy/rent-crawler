from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from bson import ObjectId
from mongoengine.queryset.visitor import Q

from .models import RentObject
from .serializers import rent_objects_schema

blueprint = Blueprint('core', __name__, url_prefix='/api/')
api = Api(blueprint)

DEFAULT_PAGE_SIZE = 20


rent_search_parser = reqparse.RequestParser()
rent_search_parser.add_argument('page', type=int, default=1)
rent_search_parser.add_argument('order_by', choices=('price', '-price', 'date', '-date'))
rent_search_parser.add_argument('rooms', type=int)
rent_search_parser.add_argument('low_price', type=int)
rent_search_parser.add_argument('high_price', type=int)
rent_search_parser.add_argument('city_district', type=ObjectId)
rent_search_parser.add_argument('search')


class RentObjectsList(Resource):

    def get(self):
        args = rent_search_parser.parse_args()
        page = args.get('page')
        order_by = args.get('order_by')
        city_district = args.get('city_district')
        rooms = args.get('rooms')
        low_price = args.get('low_price')
        high_price = args.get('high_price')
        search = args.get('search')

        rent_objects_qs = RentObject.objects

        filters = Q()

        if rooms:
            filters = filters & Q(rooms=rooms)
        if low_price:
            filters = filters & Q(price__gte=low_price)
        if high_price:
            filters = filters & Q(price__lte=high_price)
        if city_district:
            filters = filters & Q(city_district=city_district)
        if search:
            search_filter = Q(title__icontains=search) | Q(text__icontains=search)
            filters = filters & search_filter

        if order_by:
            order_by = order_by.replace('date', 'id') if 'date' in order_by else order_by
        else:
            order_by = '-id'

        rent_objects_qs = rent_objects_qs\
            .filter(filters)\
            .order_by(order_by)\

        rent_objects = rent_objects_qs\
            .skip((page - 1) * DEFAULT_PAGE_SIZE)\
            .limit(DEFAULT_PAGE_SIZE)\
            .select_related()
        return {
            'data': rent_objects_schema.dump(rent_objects).data,
            'count': rent_objects_qs.count()
        }


api.add_resource(RentObjectsList, 'rent-objects')
