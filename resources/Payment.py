from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError
        
from sqlalchemy import exc

# from models import OrderModel,OrderServicesModel,ServiceModel,ClientModel,CraftsmanModel
from Schemas import walletSchema ,paymentSchema ,orderSchema
from models import PaymentModel,WalletModel,CraftsmanModel,OrderModel,ClientModel
# from resources.RequestFunctions import  order_summary , calculate_order_total


blp = Blueprint("Request payment", "Request payment",
                description="Request payment and order summary")


   
@blp.route("/Payment/<int:order_id>")
class OrderPayment(MethodView):
    def get(self,order_id):
        order=OrderModel.query.filter_by(order_id=order_id).first()
        if not order :
         return jsonify({"Message":"Order not found "}),404
      
        if order.is_finished == False:
           return jsonify({"Message":"Order has to be closed first "}),200
        
        exist=PaymentModel.query.filter(
            PaymentModel.order_id==order_id,
            PaymentModel.total==order.total
            ).first()
        if exist:
            abort(409,message="This order has been paid already check your account ")

        wallet=WalletModel.query.filter_by(craftsman_id=order.craftsman_id).first()
        if not wallet :
            abort(404,message="wallet not found")

        # Record that payment in the payment model
        Payment=PaymentModel(
            order_id=order_id,   
            total=order.total
        )
        db.session.add(Payment)
           

      
        # Give the craftsman his balance
        wallet.balance=wallet.balance + (order.total * 0.80)


        client=ClientModel.query.filter_by(id=order.client_id).first()
        craftsman=CraftsmanModel.query.filter_by(id=order.craftsman_id).first()
      
        serialized_order=orderSchema().dump(order)
        serialized_order['client_name']=client.name
        serialized_order['craftsman_name']=craftsman.name
        # return serialized_order

        serialized_payment=paymentSchema().dump(Payment)  
      
        db.session.commit()
        return jsonify({
            "Order summary ": serialized_order,
            "payment":serialized_payment,
            }),200

