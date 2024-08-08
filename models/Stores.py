from db import db

class StoreModel(db.Model):
    __tablename__="StoreModel"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    description= db.Column(db.String(255), nullable=True)
    location=db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=True)


    admin_id=db.Column(db.Integer,db.ForeignKey("AdminModel.id"),nullable=False)

    admin_stores=db.relationship(
            "AdminModel",back_populates="adminAddStores")
    
    items=db.relationship(
        "ItemModel",back_populates="stores",lazy="dynamic",cascade="all, delete-orphan")
    
    coupon=db.relationship(
        "CouponModel",back_populates="store",lazy="dynamic",cascade="all, delete-orphan"
    )