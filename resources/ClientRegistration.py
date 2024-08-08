from flask.views import MethodView
from flask import request ,jsonify
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token



from sqlalchemy.exc import SQLAlchemyError

from db import db

from models import ClientModel,UserModel

from Schemas import ClientSchema


blp = Blueprint("Clients", "client", description="operation on client")



@blp.route("/ClientRegistration")
class UserRegister(MethodView):
    @blp.arguments(ClientSchema)
    # @blp.response(201,ClientSchema)
    # any data coming from the user take it in the scehma 
    # and pass it to the method as parameter 
    def post(self, Client_data):

        # check if there is similar UN
        if UserModel.query.filter(UserModel.username == Client_data["username"]).first():
            abort(403,
                  message="username taken, try again."
                  )
        

        Client = ClientModel(
            name=Client_data["name"],
            username=Client_data["username"],
            Email=Client_data["Email"],
            password=pbkdf2_sha256.hash(Client_data["password"]),
            phone=Client_data["phone"],
            user_type=Client_data["user_type"]
        )

        db.session.add(Client)
        db.session.commit()
        access_token = create_access_token(identity=Client.id)
        return jsonify({
            "jwt": access_token,
            "user": {
                "id": Client.id,
                "name": Client.name,
                "username": Client.username,
                "email": Client.Email,
                "phone": Client.phone,
                "user_type": Client.user_type
            }
        }), 201
