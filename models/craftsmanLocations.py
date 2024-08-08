from db import db 

class CraftsmanLocationModel(db.Model):
    __tablename__="CraftsmanLocationModel"

    
    id=db.Column(db.Integer, primary_key=True)

    craftsman_id=db.Column(db.Integer,db.ForeignKey("CraftsmanModel.id",ondelete='CASCADE'),nullable=False)
    operatingLocation_id=db.Column(db.Integer,db.ForeignKey("LocationModel.id",ondelete='CASCADE'),nullable=False)
