from flask.views import MethodView
from flask import request ,jsonify
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token,jwt_required , get_jwt_identity


from db import db

from models import UserModel,CraftsmanModel,CategoryModel,WalletModel
# from marshmallow import Schema, fields


from Schemas import CraftsmanSchema


blp = Blueprint("Craftsman", "crafts", description="Craftsman registration")



@blp.route("/CraftsmanRegistration")
class CraftsmanRegister(MethodView):
    @blp.arguments(CraftsmanSchema)
    @blp.response(201,CraftsmanSchema)
    def post(self, Craftsman_data):

        # check if there is similar UN
        if UserModel.query.filter(UserModel.username == Craftsman_data["username"]).first():
            abort(403,
                  message=
                  "username taken, try again."
                  )
       
        category=CategoryModel.query.filter(
            CategoryModel.name==Craftsman_data["category_name"]).first()
        

        
      
        Craftsman = CraftsmanModel(
                name=Craftsman_data["name"],
                username=Craftsman_data["username"],
                Email=Craftsman_data["Email"],
                password=pbkdf2_sha256.hash(Craftsman_data["password"]),
                phone=Craftsman_data["phone"],
                # front_image=Craftsman_data["front_image"],
                # back_image=Craftsman_data["back_image"],
                user_type=Craftsman_data["user_type"],
                category_id=category.id,
                completed_orders=0
        
            )
        

        Craftsman.category_name = category.name  # Set the category_name explicitly

        db.session.add(Craftsman)

        db.session.commit()

        wallet=WalletModel(
            craftsman_id=Craftsman.id,
            balance=0.0)
        db.session.add(wallet)
        db.session.commit()


        access_token = create_access_token(identity=Craftsman.id)

        serialized_craftsman = CraftsmanSchema().dump(Craftsman)

        return jsonify({"user":serialized_craftsman ,"jwt": access_token,}),201
    
@blp.route("/Craftsman/profile")
class GetCraftsman(MethodView):
    @jwt_required()
    @blp.response(201,CraftsmanSchema)
    def get(self):
        craftsman_id=get_jwt_identity()

        craftsman=CraftsmanModel.query.filter_by(id=craftsman_id).first()

        return craftsman
