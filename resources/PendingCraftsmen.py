from flask.views import MethodView
from flask import jsonify,request
from flask_smorest import Blueprint, abort
from db import db

from flask_mail import Message
from app import mail

from models import CraftsmanModel,UserModel
from Schemas import CraftsmanSchema,PendingCraftsmenSchema,MailSchema

blp = Blueprint("Get all pending craftsmen", "pending", description="List all the pending craftsmen data before loging to the app")


@blp.route("/Admin/Pending")
class PendingCraftsmen(MethodView):
    @blp.response(200,PendingCraftsmenSchema(many=True))
    def get(self):
        craftsmen=CraftsmanModel.query.filter(CraftsmanModel.Pending=="TRUE").all()
        if not craftsmen :
            abort(404,message="No craftsmen are found")
        return  craftsmen


@blp.route("/Admin/<int:craftsman_id>/Verification")
class AcceptingCraftsman(MethodView):
   def put(self, craftsman_id):
        craftsman = CraftsmanModel.query.get_or_404(craftsman_id)

        craftsman.Pending = False

        db.session.commit()

        return {
            "Message": "Accepted."
        },200
   



@blp.route("/Admin/Rejection")
class RejectingCraftsman(MethodView):
    @blp.arguments(MailSchema)# {cratftsman_id , subject  , body }
    def post (self,mail_data):
        if not mail_data["body"]:
            return jsonify({"Message":"Missing body"})
        #check if the craftsman exsits
        # user=UserModel.query.filter_by(id=mail_data["cratftsman_id"]).first()
        craftsman=CraftsmanModel.query.filter_by(id=mail_data["cratftsman_id"]).first()
        if not craftsman :
            abort(404,message=" Craftsman Not found!")
        # try       
        try:

            msg = Message(mail_data["subject"], recipients=[craftsman.Email])
            msg.body = mail_data["body"]
            mail.send(msg)  # Ensure msg is defined before sending  

            db.session.delete(craftsman)
            db.session.commit()
           
            return jsonify({'status': 'Email sent successfully and the craftsman data has been deleted.'}), 200
        
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
      


