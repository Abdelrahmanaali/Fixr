from flask import  request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import LocationModel,AdminModel
from Schemas import SetlocationSchema,ReturnlocationSchema

blp = Blueprint("Add operating locations", "op areas", description="Admin add locations")


@blp.route("/Admin/SetNewLocations")
class SetLocation(MethodView):
    @jwt_required()
    @blp.arguments(SetlocationSchema)
    def post(self, location_data):
        admin_id=get_jwt_identity()
        if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role !="operational").first():
            abort(401,
                   message="Permission denied. Only operational admins can add operating areas."

                  )

        try:
            created_locations = []

            for location_name in location_data["locations"]:
                location_name_lower = location_name.lower()  # Convert to lowercase
                existing_location = LocationModel.query.filter_by(
                    name=location_name_lower).first()

                if existing_location:
                    continue

                location = LocationModel(
                    name=location_name_lower,admin_id=admin_id)
                
                db.session.add(location)
                created_locations.append(location_name_lower)

            db.session.commit()
            if not created_locations:
                return {"message": " No new locations were added , all the locations are saved already"}, 200
         
            return {"Added locations": created_locations}, 201

        except IntegrityError:
            abort(400,
                  message="All the locations are already exsit")

        except SQLAlchemyError:
            abort(500,
                  message="an error occured while saving the locations\n Check the docs and re-enter them")


@blp.route("/OperatingLocations")
class AllOperationgLocations(MethodView):
    @blp.response(201,ReturnlocationSchema(many=True))
    def get(self):
        try:
            OperatingLocations=LocationModel.query.all()
            return OperatingLocations
        except SQLAlchemyError:
            abort(500,
                  message="an error occured")

@blp.route("/Admin/OperatingLocations/<int:location_id>")
class deleteLocation(MethodView):
    def delete(self,location_id):
        location=LocationModel.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return{"message":"Location deleted."},200
   