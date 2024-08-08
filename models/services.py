from db import db

class ServiceModel(db.Model):
    __tablename__="ServicesModel"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price=db.Column(db.Integer,nullable=False)

    admin_id=db.Column(db.Integer,db.ForeignKey("AdminModel.id"),nullable=False)

    category_id=db.Column(db.Integer,db.ForeignKey("CategoryModel.id"),nullable=False)

    service=db.relationship(
        "AdminModel",back_populates="adminAddService")
    
    category=db.relationship(
        "CategoryModel",back_populates="CategoryService")
    
    orders_services=db.relationship("OrderModel",back_populates="order_services",secondary="OrderServicesModel")
    


