from db import db

class OrderServicesModel(db.Model):
    __tablename__="OrderServicesModel"
    id=db.Column(db.Integer, primary_key=True)

    order_id=db.Column(db.Integer,db.ForeignKey("OrderModel.order_id",ondelete='CASCADE'),nullable=False)
    service_id=db.Column(db.Integer,db.ForeignKey("ServicesModel.id"),nullable=False)

