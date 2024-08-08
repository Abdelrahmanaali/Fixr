from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError

from models import ServiceModel,OrderServicesModel,CraftsmanModel,CraftsmanLocationModel,LocationModel,OrderModel
from Schemas import FilteredCraftsmen,orderServices,RequestedCraftsman,CraftsmanReview
from resources.RequestFunctions import calculate_order_total , avg_rating ,Calculate_rate,Craftsman_feedback


blp = Blueprint("Craftsmen List for request", "Craftsmen for reqest",
                description="list of craftsmen")


  
@blp.route("/craftsmenForOrder")
class RequestCraftsmen(MethodView):
    # @jwt_required()
    @blp.arguments(FilteredCraftsmen)
    def get(self,order_data):


        order=OrderModel.query.filter_by(order_id=order_data["order_id"]).first()
        if not order : 
             abort(404 , message = "Order Not Found.")
        # order_details=OrderModel(
        #      area=order_data["order_id"],
        #      additional=order_data["additional"]
        # )
        # db.session.add(order_details)
        # db.session.commit()
        area=LocationModel.query.filter(LocationModel.name==order.area).first()
        if not area :
            return jsonify({"Message":"We do not operate in " + order.area + " yet!"}),200
           #abort(200,message="We do not operate in " + order_data["city"] + " yet!")

        services=OrderServicesModel.query.filter(OrderServicesModel.order_id==order_data["order_id"]).all()
        serialized_service=orderServices(many=True).dump(services)

         # Get the categories of the services in the order
        service_ids = [service.service_id for service in services]
        service_categories = ServiceModel.query.filter(ServiceModel.id.in_(service_ids)).all()
        category_ids = {service.category_id for service in service_categories}

        craftsmen = CraftsmanModel.query.join(CraftsmanLocationModel).join(LocationModel).filter(
            LocationModel.name == order.area,
            CraftsmanModel.is_available==True,
            CraftsmanModel.Pending==False,
            CraftsmanModel.category_id.in_(category_ids)
        ).all()

        if not craftsmen:
            return jsonify({"Message":"Sorry but it seems like no craftsmen are available in the moment, Please try again in a while."}),200
            #abort(404,Message="Sorry but it seems like no craftsmen are available in the moment, Please try again in a while.")

        serialized_craftsman = RequestedCraftsman(many=True).dump(craftsmen)

        order_total=calculate_order_total(order_data["order_id"]) # OK
        
        for craftsman in serialized_craftsman:
         
            craftsman['rating'] = avg_rating(craftsman['id'])
            if craftsman['rating'] is None or craftsman['rating'] == 0:
                    craftsman['rating'] = 1
            craftsman['fair'] = Calculate_rate(craftsman["rating"], order_total)
            # craftsman['reviews'] = Craftsman_feedback(craftsman['id'])               
        return jsonify({
                        "Craftsmen": serialized_craftsman,
                        # "services":serialized_service,
                        "Total of order":order_total})