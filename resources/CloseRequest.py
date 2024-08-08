from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import OrderModel,CraftsmanModel,RatingModel

from resources.RequestFunctions import calculate_order_total,avg_rating,Calculate_rate
from Schemas import CloseRequestSchema
blp = Blueprint("Clients Close request", "Clients Closes craftsman",
                description="Client or craftsman closes the request.")

@blp.route("/CloseRequest/<int:order_id>")
class CloseRequest(MethodView):
    @blp.arguments(CloseRequestSchema)
    def post(self,order_data,order_id):
        # Get the order instance
        order=OrderModel.query.filter_by(order_id=order_id).first()
        # Validate if exsit
        if not order :
            abort(404,message="Order not found check the order number .")
        # Check if already closed
        if order.is_finished==True:
            return{"Message":"The order is already closed"}
        # If a craftsman is not assigned to it 
        if not order.craftsman_id:
            return{"Message":"The order has no craftsman it cannot be closed"}
        # Get the price choosen by the client 
        craftsman_id=order.craftsman_id # Get the craftsman of the order
        rate=avg_rating(craftsman_id) # Get the old rating of this craftsman
        order_total=calculate_order_total(order_id) # get the real total of the order
        total=Calculate_rate(rate,order_total)  # get the total of the order + the bonus 
        order.total=total # assign the total with the order

        # Make the  rate 
        order_rate=RatingModel(
            order_id=order_id,
            feedback=order_data["feedback"],
            rating=order_data["rate"]
        )
        db.session.add(order_rate)

        # Close the order
        order.is_finished=True
        if order.is_finished == True: #check if true 
            craftsman=CraftsmanModel.query.filter_by(id=craftsman_id).first() # Get the craftsman instance
            if craftsman.completed_orders==None: # avoid nulls 
                craftsman.completed_orders=0
            craftsman.completed_orders = craftsman.completed_orders + 1
            craftsman.is_available=True # return avaialbe again
            
            
            # craftsman.rate=rate
   
        db.session.commit()
        return jsonify({"Message":"Thanks for using fixr app"
                        ,"Note":"Now craftsmen is avaialble again"}),200