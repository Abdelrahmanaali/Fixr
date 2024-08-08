from flask import  request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db



from marshmallow import Schema, fields, ValidationError

class OperatingLocationSchema(Schema):
    locations = fields.List(fields.Str(), required=True)

class OperatingLocation(Schema):
    name = fields.Str()


from models import LocationModel,CraftsmanModel


blp = Blueprint("Craftsman locations", "Craftsmen operating locations",
                 description="craftsman selecting multiple operating locations")


@blp.route("/Craftsman/Locations")
class CraftsmanLocations(MethodView):
    @jwt_required()
    # @blp.response(201,OperatingLocation(many=True))
    def post(self):
        craftsman_id = get_jwt_identity()
        craftsman = CraftsmanModel.query.filter(CraftsmanModel.id==craftsman_id).first()
        if not craftsman:
            return {"message": "Craftsman not found"}, 404

        try:
            data = OperatingLocationSchema().load(request.json)
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        for location_name in data["locations"]:
            location = LocationModel.query.filter_by(name=location_name).first()
            if not location:
                return {"message": f"Location '{location_name}' not found"}, 404

            # Check if the location is already associated with the craftsman
            if location not in craftsman.operatingLocation:
                craftsman.operatingLocation.append(location)

        db.session.commit()
        # return craftsman.operatingLocation
        return {"message": "Operating locations added successfully"}, 201

    