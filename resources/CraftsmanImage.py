from flask.views import MethodView
from flask import request ,jsonify,abort
from flask_smorest import Blueprint

from db import db

from flask_jwt_extended import jwt_required, get_jwt_identity

import cloudinary
from cloudinary.uploader import upload


from models import CraftsmanModel



blp = Blueprint("crafstman upload image ", "upload img", description="upload process")

@blp.route("/Craftsman/Upload")
class uploadImage(MethodView):
    @jwt_required()
    def post(self):

        #Get the craftsman if found based on his id in the jwt
        craftsman_id = get_jwt_identity()
       
        craftsman = CraftsmanModel.query.filter(CraftsmanModel.id == craftsman_id).first()

        # if the craftsman exists:
        if craftsman: 
            # Check if both image attribute is empty
            if not craftsman.front_image and not craftsman.back_image:
                #request the file to be uploaded
                front_image=request.files["front"]
                back_image = request.files["back"]
               
                if front_image and back_image: #if the user provided file 

                    # Front result is a dictionary 
                    front_result = upload(front_image, quality=60)#func upload take the photo to be uploaded
                    front_image_url=front_result['secure_url'] #the key secure_url is in the dictionary front_result
                    craftsman.front_image=front_image_url

                    back_result = upload(back_image, quality=60)
                    back_image_url = back_result['secure_url']
                    craftsman.back_image=back_image_url

                    db.session.commit()

                    return jsonify({'Front image url': front_image_url, "Back image url": back_image_url}), 200
                
                else:
                      return jsonify({'error': 'No file provided, Please make sure that the two photos are uploaded.'}), 400
                   
            else:
                return jsonify({'error': 'Both image already uploaded'}), 400
              
            
        return {"Message": "This account is not found.Try signing up again."}, 404



    @blp.route("/Craftsman/ProfilePicture")
    class CraftsmanProfilePicture(MethodView):
        @jwt_required()
        def put(self):

            craftsman_id = get_jwt_identity()

            craftsman = CraftsmanModel.query.filter(CraftsmanModel.id == craftsman_id).first()

            if not craftsman:
                abort(404,message="Not found.")

            profile_pic=request.files["profile"]
            if profile_pic:
                profile_result=upload(profile_pic)

                profile_pic_url=profile_result["secure_url"]

                craftsman.profile_pic=profile_pic_url

                db.session.commit()
                return{"Message":"Uploaded successfully"}
            
            return {"message":"No profile pic where uploaded."}
        






