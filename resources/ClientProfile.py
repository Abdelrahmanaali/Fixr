from flask.views import MethodView
from flask import request ,jsonify,abort
from flask_smorest import Blueprint

from db import db

from flask_jwt_extended import jwt_required, get_jwt_identity

import cloudinary
from cloudinary.uploader import upload


from models import CraftsmanModel,ClientModel



blp = Blueprint("Client upload image ", "upload img", description="upload process")
@blp.route("/Client/ProfilePicture")
class ClientProfilePicture(MethodView):
        @jwt_required()
        def put(self):

            client_id = get_jwt_identity()

            client = ClientModel.query.filter(ClientModel.id == client_id).first()

            if not client:
                abort(404,message=" Client Not found.")

            profile_pic=request.files["profile"]

            if profile_pic:
                profile_result=upload(profile_pic)

                profile_pic_url=profile_result["secure_url"]

                client.profile_pic=profile_pic_url

                db.session.commit()
                return{"Message":"Uploaded successfully"}
            
            return {"message":"No profile pic where uploaded."}