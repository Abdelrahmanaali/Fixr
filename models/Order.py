from db import db

class OrderModel(db.Model):
    __tablename__="OrderModel"
    order_id = db.Column(db.Integer, primary_key=True)
    client_id=db.Column(db.Integer,db.ForeignKey("ClientModel.id"),nullable=False)
    craftsman_id=db.Column(db.Integer,db.ForeignKey("CraftsmanModel.id"),nullable=True)
    total=db.Column(db.Integer,nullable=True)
    is_finished=db.Column(db.Boolean, nullable=False,
                             default=False)
    date=db.Column(db.DateTime, nullable=False)
    area=db.Column(db.String(255), unique=False, nullable=True)
    additional=db.Column(db.String(255), unique=False, nullable=True)

    
    client_order=db.relationship("ClientModel",back_populates="order")
    craftsman_order=db.relationship("CraftsmanModel",back_populates="orders")

    order_services=db.relationship("ServiceModel",
                                   back_populates="orders_services",
                                   secondary="OrderServicesModel"                                   )

    rating = db.relationship("RatingModel", back_populates="order", uselist=False)