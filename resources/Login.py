from flask.views import MethodView
from flask import request ,jsonify
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token,jwt_required , get_jwt_identity




from models import UserModel,CraftsmanModel

from Schemas import UserLoginSchema


blp = Blueprint("Login", "login", description="Login process")



@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self,user_data):
        user = UserModel.query.filter(
            (UserModel.phone == user_data["handler"]) | (UserModel.username == user_data["handler"])
        ).first() 

        if user:
            if user.user_type == "craftsman":
                craftsman = CraftsmanModel.query.filter(
                   ( CraftsmanModel.phone==user_data["handler"]) | (CraftsmanModel.username==user_data["handler"])
                    ).first()
                if craftsman and craftsman.Pending:
                    return {"message": "Hello " + craftsman.username + "! Your account as a craftsman is under supervision."}, 200

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"jwt": access_token , "message:":"welcome "+user.username}, 200

        abort(401, message="Invalid credentials.")





        # if UserModel.query.filter(UserModel.user_type == "craftsman").first():
        #     if CraftsmanModel.query.filter(CraftsmanModel.Pending=="TRUE").first():
        #         return{"message":"your account as craftsman is under supervision"}
            
            
#---------------------OLD LOGIN----------------------------------------
# @blp.route("/login")
# class UserLogin(MethodView):
#     @blp.arguments(UserLoginSchema)
#     def post(self,user_data):
    
#         if "username" in user_data:    
#             user = UserModel.query.filter(
#                     UserModel.username == user_data["username"]
#                 ).first()
            
#         elif "phone" in user_data:
#             user = UserModel.query.filter(
#                     UserModel.phone == user_data["phone"]
#                 ).first()


#         if user and pbkdf2_sha256.verify(user_data["password"], user.password):
#             access_token = create_access_token(identity=user.id)
#             return {"jwt": access_token , "message:":"welcome "+user.username}, 200

#         abort(401, message="Invalid credentials.")

