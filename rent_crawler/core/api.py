from flask import Blueprint
from flask_restful import Api, Resource

from .models import RentObject
from .serializers import rent_objects_schema

blueprint = Blueprint('core', __name__, url_prefix='/api/')
api = Api(blueprint)


class RentObjectsList(Resource):

    def get(self):
        rent_objects = RentObject.objects.all()
        return rent_objects_schema.dump(rent_objects)


api.add_resource(RentObjectsList, 'rent-objects')
