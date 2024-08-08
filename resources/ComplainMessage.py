from flask.views import MethodView
from flask_smorest import Blueprint,abort
from flask import request,jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


from db import db
from models import MessageModel, UserModel
from Schemas import PlainMessageSchema,MessageSchema


blp = Blueprint("Messages", "message",
                description="Client sends messages to the admins")


@blp.route("/SendMessage")
class Messages(MethodView):
    @jwt_required()
    def post(self):
        message_data = request.json
        user = get_jwt_identity()  # Get the ID from token since its based on the identifier=id
        user_object = UserModel.query.filter(UserModel.id == user).first()
        user_type = user_object.user_type
        message = MessageModel(
            user_id=user,
            user_type=user_type,
            MessageDetail=message_data["message"],
            ContactEmail=message_data["contact-email"]
        )
        db.session.add(message)
        db.session.commit()
        return {"message": "message sent"}, 201



@blp.route("/ViewMessages")
class ViewMessages(MethodView):
    @jwt_required()
    @blp.response(201,PlainMessageSchema(many=True))
    def get(self):
        admin=get_jwt_identity()
        if UserModel.query.filter(UserModel.id==admin,UserModel.user_type!="admin").first():
            abort(401,
                  message="Permission denied.")
        return MessageModel.query.all()



@blp.route("/MyProfile/Messages")
class personnelMessages(MethodView):
    @jwt_required()
    @blp.response(201,MessageSchema(many=True))
    def get(self):
        user_id=get_jwt_identity()
        Messages=MessageModel.query.filter_by(user_id=user_id).all()
        if not Messages:
            return jsonify( {"Messages":"No messages yet."}),404
        return Messages

  