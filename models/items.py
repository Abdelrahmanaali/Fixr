from db import db

class ItemModel(db.Model):
    __tablename__="ItemModel"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255) ,nullable=False)
    price=db.Column(db.Float(precision=2),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    image= db.Column(db.String(255), nullable=True)

    store_id=db.Column(db.ForeignKey("StoreModel.id", ondelete='CASCADE'),nullable=False)

    # admin_id=db.Column(db.ForeignKey("AdminModel.id"),nullable=False)


    stores=db.relationship(
        "StoreModel",back_populates="items")


    
