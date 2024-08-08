from db import db 

class PaymentModel(db.Model):
    __tablename__="PaymentMdel"
    id= db.Column(db.Integer, primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey("OrderModel.order_id",ondelete='CASCADE'),nullable=False)
    total=db.Column(db.Integer,nullable=False)
    # client_id=db.Column(db.Integer,db.ForeignKey("ClientModel.id"),nullable=False)

    # payment=db.relationship("ClientModel",back_populates="payments")
    
