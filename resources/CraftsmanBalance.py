from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError
        
from sqlalchemy import exc

# from models import OrderModel,OrderServicesModel,ServiceModel,ClientModel,CraftsmanModel
from Schemas import walletSchema ,paymentSchema ,orderSchema
from models import PaymentModel,WalletModel,CraftsmanModel
# from resources.RequestFunctions import  order_summary , calculate_order_total


blp = Blueprint("Craftsman balance", "craftsman balance",
                description="craftsman balance")

@blp.route("/Craftsman/balance")
class craftsmanBalance(MethodView):
    @jwt_required()
    def get(self):
        craftsman_id=get_jwt_identity()
        # craftsman=CraftsmanModel.query.filter_by(id=craftsman_id).first()
        wallet=WalletModel.query.filter_by(craftsman_id=craftsman_id).first()
        balance=wallet.balance
        return jsonify({"My balance":balance}),200