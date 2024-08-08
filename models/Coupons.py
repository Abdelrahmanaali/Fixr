from db import db 
from datetime import datetime
# from pytz import timezone
# egypt_tz = timezone('Africa/Cairo')

class CouponModel(db.Model):
    __tablename__="CouponModel"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.Integer,nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("StoreModel.id" ,ondelete='CASCADE'), nullable=False)



    store=db.relationship("StoreModel",back_populates="coupon")
