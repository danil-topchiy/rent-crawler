from flask import Blueprint
from flask_restful import Api, Resource

from .models import RentObject
from .serializers import rent_objects_schema

blueprint = Blueprint('core', __name__, url_prefix='/api/')
api = Api(blueprint)


class RentObjectsList(Resource):

    def get(self):
        rent_objects_qs = RentObject.objects.filter()
        rent_objects = rent_objects_qs.select_related()
        return {
            'data': rent_objects_schema.dump(rent_objects),
            'count': rent_objects_qs.count()
        }


api.add_resource(RentObjectsList, 'rent-objects')
