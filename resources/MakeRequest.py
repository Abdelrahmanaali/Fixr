from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError

from models import OrderModel,ServiceModel,OrderServicesModel
from Schemas import ServiceListSchema



blp = Blueprint("Clients make request", "Clients make request",
                description="Client make request")



@blp.route("/request")
class Request(MethodView):
    @jwt_required()
    @blp.arguments(ServiceListSchema)
    def post(self,service_data):
        # Get the client identiy
        client_id=get_jwt_identity()
        """
        #Get the client Location 
        # client_location=ClientLocationModel.query.filter_by(client_id=client_id).first()
        # Get the client city to get all the craftsmen in this city
        # city=client_location.city
        # Make an order with the client id to fill it with the services
        """
        order=OrderModel(
            client_id=client_id,
            date=service_data["date"],
            area=service_data["area"],
            additional=service_data["additional"]
        )

        db.session.add(order)
        
        try:
            # Loop through each service in the list 
            for service in service_data["services"]:
                # Check if each service is available
                new_service=ServiceModel.query.filter_by(name=service).first()
                if not new_service : # If not found:
                    abort(404 , message="service not found")
                # if the service is found :
                # fill all the services provided by the client to the order he just made
                add_service=OrderServicesModel(
                    order_id=order.order_id,
                    service_id=new_service.id)
                
                db.session.add(add_service)

         
        except SQLAlchemyError:
            abort(500,message='internal server error')

        db.session.commit()    

        """
        # craftsmen = CraftsmanModel.query.join(CraftsmanLocationModel).join(LocationModel).filter(
                #     LocationModel.name == city,CraftsmanModel.is_available==True
                # ).all()
                # serialized_craftsman = CraftsmanSchema(many=True).dump(craftsmen)  
        """
        return jsonify(
            {"message": "Order has been added.","Order number ":order.order_id})