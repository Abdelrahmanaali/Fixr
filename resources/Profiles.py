from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError


from models import UserModel,CraftsmanModel,ClientModel
from Schemas import CraftsmanSchema,ClientSchema

blp=Blueprint("Profile","profile",description="Get profile")

@blp.route("/Profile")
class profile(MethodView):
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        user=UserModel.query.filter(UserModel.id==user_id).first()
        if user :
            if user.user_type == "craftsman":
                craftsman=CraftsmanModel.query.filter_by(id=user_id).first()
                serialized_craftsman=CraftsmanSchema().dump(craftsman)
                return{"User":serialized_craftsman}
            elif user.user_type == "client":
                client=ClientModel.query.filter_by(id=user_id).first()
                serialized_client=ClientSchema().dump(client)
                return{"user":serialized_client}
        return{"Message":"user not found"},404