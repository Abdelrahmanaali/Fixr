from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError

from models import OrderModel
from Schemas import OrderServicesOnlySchema
 
blp = Blueprint("OrderService", "OrderDetails",
                description="all services in order.")
@blp.route("/OrderServices/<int:order_id>")
class see(MethodView):
    def get(self,order_id):
        order=OrderModel.query.filter_by(order_id=order_id).first()
        if not order :
            abort(404,message="Order not found check the order number .")

        result=OrderServicesOnlySchema().dump(order)
        return jsonify({"services":result})
    