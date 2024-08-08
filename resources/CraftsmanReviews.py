from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError

from models import CraftsmanModel,ClientModel
from Schemas import CraftsmanReview
from resources.RequestFunctions import Craftsman_feedback


blp = Blueprint("Craftsmen Reivews", "Craftsmen reviews",
                description="list of reviews of the craftsman")

@blp.route("/CraftsmanReviews/<int:craftsman_id>")
class CraftsmanReviews(MethodView):
    def get(self,craftsman_id):
        craftsman=CraftsmanModel.query.filter_by(id=craftsman_id).first()
        if not craftsman :
            abort(404,message="Craftsman not found.")

        feedbacks=Craftsman_feedback(craftsman_id)
        if not feedbacks:
            return jsonify({"Message":"No reviews yet"}),200
        
        serialized_feedbacks=CraftsmanReview(many=True).dump(feedbacks)
        
        for review in serialized_feedbacks:
            # client=ClientModel.query.filter_by(id=review["client_id"]).first()
            # if client:
                # review['Client_name'] = client.name 
                review['craftsman_name'] = craftsman.name 
        return jsonify({"Reviews":serialized_feedbacks}),200 