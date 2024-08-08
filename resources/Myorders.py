from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError

from models import UserModel,OrderModel
from Schemas import NewOrderSchema,CloseRequestSchema,CraftsmanReview
from resources.RequestFunctions import order_summary


blp = Blueprint("My orders ", "My order",
                description="Chechk the orders")


@blp.route("/MyOrders")
class myOrders(MethodView):
    @jwt_required()
    def get (self):
        user_id=get_jwt_identity()
        
        user=UserModel.query.filter_by(id=user_id).first()
        if user.user_type =="client":
            orders=OrderModel.query.filter(OrderModel.client_id==user.id).all()
            if orders:
                serialized_orders=NewOrderSchema(many=True).dump(orders)
                return jsonify({"My orders": serialized_orders})
            return jsonify({"Message":"No orders for this client yet!"})
        
        elif user.user_type =="craftsman":
            orders=OrderModel.query.filter(OrderModel.client_id==user.id).all()
            if orders:
                serialized_orders=NewOrderSchema(many=True).dump(orders)
                return jsonify({"My orders": serialized_orders})
            return jsonify({"Message":"No orders for this Craftsman yet!"})
        
        else:
            return jsonify({"Message":"User not found."})

        
# @blp.route("/func/<int:craftsman_id>")
# class testfunction(MethodView):
#     def get(self,craftsman_id):
#         feedbacks=Craftsman_feedback(craftsman_id)
#         serialized_feedbacks=CraftsmanReview(many=True).dump(feedbacks)
#         # t=calculate_order_total(order_id)
#         # c=avg_rating(craftsman_id)
#         # rates=Calculate_rate(craftsman_id,order_id)
#         return{"feedback":serialized_feedbacks}
    
        
# @blp.route("/func/<int:order_id>")
# class testfunction(MethodView):
#     @blp.arguments(CloseRequestSchema)
#     def get(self,order_data,order_id):
#         order=order_id
#         rate=order_data["rate"]
#         return{"rates":rate,"order number":order}
    
