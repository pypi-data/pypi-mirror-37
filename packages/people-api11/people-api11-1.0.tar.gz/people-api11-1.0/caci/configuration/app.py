from flask import Blueprint
from flask_restful import Api
from caci.controler.Profiles import ProfilesList, ProfileIn, ProfileDelete, ProfileJson

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(ProfilesList, '/people/')
# JsonFormat
api.add_resource(ProfileJson, '/people/json/<p>')
# Search
api.add_resource(ProfileIn, '/people/search/<username>')
# Delete
api.add_resource(ProfileDelete, '/people/<username>')