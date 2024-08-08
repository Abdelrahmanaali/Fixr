from db import db 
from datetime import datetime,UTC

class RatingModel(db.Model):
    __tablename__ = "RatingModel"
    id = db.Column(db.Integer, primary_key=True )   
    order_id=db.Column(db.Integer,db.ForeignKey("OrderModel.order_id",ondelete='CASCADE'),nullable=False)
    rating=db.Column(db.Float(precision=2), nullable=False)
    feedback=db.Column(db.String(255), unique=False, nullable=True)
    # date = db.Column(db.DateTime, default=datetime.now)
    order = db.relationship("OrderModel", back_populates="rating")




 