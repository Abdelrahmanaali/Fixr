# from db import db 


# class ClientLocationModel(db.Model):
#     __tablename__="ClientLocationModel"
   
#     id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(255),nullable=False)
#     district = db.Column(db.String(255),nullable=False)
#     building = db.Column(db.String(255),nullable=False) 
#     street = db.Column(db.String(255),nullable=False)
#     floor = db.Column(db.String(255),nullable=False)
#     apartment = db.Column(db.String(255),nullable=False)
#     Long = db.Column(db.String(255),nullable=False)
#     Lat = db.Column(db.String(255),nullable=False)
#     additional = db.Column(db.String(255),nullable=True)


    

#     client_id=db.Column(db.Integer,db.ForeignKey("ClientModel.id"),nullable=False)
#     selctedLocation=db.relationship(
#         "ClientModel",back_populates="clientLocation")
