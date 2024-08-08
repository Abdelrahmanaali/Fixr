from db import db


class LocationModel(db.Model):
    __tablename__ = "LocationModel"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    admin_id=db.Column(db.Integer,db.ForeignKey("AdminModel.id"),nullable=False)



    admin_locations = db.relationship(
                     "AdminModel", back_populates="adminAddLocations")
    

    craftsmanLocation=db.relationship(
        "CraftsmanModel",back_populates="operatingLocation",secondary="CraftsmanLocationModel"
    )
    


