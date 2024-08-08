# from flask import request, jsonify
# from flask.views import MethodView
# from flask_smorest import Blueprint, abort
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from db import db

# from sqlalchemy.exc import SQLAlchemyError

# from models import ClientLocationModel, ClientModel
# from Schemas import ClientLocationSchema

# blp = Blueprint("Client add locations", "Clients locations",
#                 description="Client add locations")


# @blp.route("/Client/SetLocations")
# class ClientSetLocation(MethodView):
#     @jwt_required()
#     @blp.arguments(ClientLocationSchema)
#     @blp.response(201, ClientLocationSchema)
#     def post(self, client_location):
#         client_id = get_jwt_identity()
       

#         if ClientLocationModel.query.filter(
#                 ClientLocationModel.city == client_location["city"],
#                 ClientLocationModel.district == client_location["district"],
#                 ClientLocationModel.building == client_location["building"],
#                 ClientLocationModel.street == client_location["street"],
#                 ClientLocationModel.floor == client_location["floor"],
#                 ClientLocationModel.apartment == client_location["apartment"],
#                 ClientLocationModel.additional == client_location["additional"],
#                 ClientLocationModel.Lat == client_location["lat"],
#                 ClientLocationModel.Long == client_location["long"],
#                 ClientLocationModel.client_id == client_id).first():
#             abort(409,
#                   message="This location already saved")

#         location = ClientLocationModel(
#             city=client_location["city"],
#             district=client_location["district"],
#             building=client_location["building"],
#             street=client_location["street"],
#             floor=client_location["floor"],
#             apartment=client_location["apartment"],
#             Long=client_location["long"],
#             Lat=client_location["lat"],
#             additional=client_location["additional"],
#             client_id=client_id
#         )

#         try:
#             db.session.add(location)
#             db.session.commit()
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             abort(500, message="Failed to add location")

#         client_data = ClientModel.query.filter(
#             ClientModel.id == client_id).first()

#         return jsonify({
#             "client": {
#                 "id": client_data.id,
#                 "name": client_data.name,
#                 "username": client_data.username,
#                 "email": client_data.Email,
#                 "phone": client_data.phone,
#                 "user_type": client_data.user_type
#             },
#             "location": {
#                 "id": location.id,
#                 "city": location.city,
#                 "district": location.district,
#                 "building": location.building,
#                 "street": location.street,
#                 "floor": str(location.floor),
#                 "apartment": location.apartment,
#                 "Long": location.Long,
#                 "Lat": location.Lat,
#                 "additional": location.additional
#             }
#         }), 201


# @blp.route("/Client/GetLocations")
# class GetClientLocations(MethodView):
#     @jwt_required()
#     @blp.response(200, ClientLocationSchema(many=True))
#     def get(self,):
#         client_id = get_jwt_identity()

#         locations = ClientLocationModel.query.filter(
#             ClientLocationModel.client_id == client_id).all()

#         if not locations:
#             return jsonify({"message": "No locations found for this client."}), 404
#         return locations
