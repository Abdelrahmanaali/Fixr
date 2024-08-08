from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db


from models import OrderModel,CraftsmanModel

blp = Blueprint("Clients Select Craftsman", "Clients choose craftsman",
                description="Client select craftsman by id for the request.")

      
@blp.route("/SelectCraftsman/<int:order_id>/<int:craftsman_id>")
class selectCraftsman(MethodView):
    def post(self,order_id,craftsman_id):
        craftsman=CraftsmanModel.query.filter(CraftsmanModel.id==craftsman_id).first()
        if not craftsman:
            abort(404,message=" Craftsman not found")
        if craftsman.Pending==True:
            return{"Message":"You can not assign this craftsman to the order, he is still under supervision"}
        order=OrderModel.query.filter(OrderModel.order_id==order_id).first()
        if not order :
            abort(404,message="Order not found.")
        if order.craftsman_id==craftsman_id :
            abort(409,message="craftsman already assigned to this order .")


        order.craftsman_id=craftsman.id
        craftsman.is_available=False        
        db.session.commit()
        return jsonify({"Message":" the order now has a craftsman , the craftsman is not available anymore till the request has an end "})
    