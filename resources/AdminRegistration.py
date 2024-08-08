from flask.views import MethodView
from flask import request 
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

# from flask_jwt_extended import jwt_required , get_jwt_identity

from db import db

from models import AdminModel,UserModel

from Schemas import AdminRetrival


blp = Blueprint("Admins", "admin", description="Admin registration")

@blp.route("/AdminRegistration")
class AdminRegister(MethodView):
    # @jwt_required() 
    def post(self):
        # admin_id=get_jwt_identity()
        # if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role != "super").first():
        #     abort(403,
        #            message="Permission denied. Only super admins can add other admins."

        #           )
    
        admin_data = request.get_json()
        
        # Check if there is a similar username
        if UserModel.query.filter(UserModel.username == admin_data.get("username")).first():
            abort(500,
                   message=
                   "username taken , try again.")
        
        # Separate the data to hash the user password only
        admin = AdminModel(
            name=admin_data.get("name"),
            username=admin_data.get("username"),
            Email=admin_data.get("email"),
            password=pbkdf2_sha256.hash(admin_data.get("password")),
            Role=admin_data.get("role"),
            phone=admin_data.get("phone"),
            user_type=admin_data.get("type")
        )

        db.session.add(admin)
        db.session.commit()
        # return admin
        return {"message": f"{admin.username} added successfully"}  # Return a valid response
      


@blp.route("/retrive")
class retrive(MethodView):
    @blp.response(201,AdminRetrival(many=True))
    def get(self):
        admins=AdminModel.query.filter(AdminModel.Role=="operational").all()
        
        return admins
     
            
    


