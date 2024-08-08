from db import db

class MessageModel(db.Model):
    __tablename__="MessageModel"
    id=db.Column(db.Integer, primary_key=True)
    ContactEmail = db.Column(db.String(255), unique=False, nullable=False)
    MessageDetail = db.Column(db.String(255), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('UserModel.id'), nullable=False)
    user_type=db.Column(db.String(255),nullable=False)

    
    user=db.relationship("UserModel",back_populates="messages")
    # MessageDate = db.Column(db.DateTime(timezone=True), server_default=func.now(), unique=False, nullable=False)
