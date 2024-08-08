from db import db


class CategoryModel(db.Model):
    __tablename__="CategoryModel"
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    details = db.Column(db.String(255), unique=True, nullable=False)


    admin_id=db.Column(db.Integer,db.ForeignKey("AdminModel.id"),nullable=False)

    admin_categories=db.relationship(
            "AdminModel",back_populates="adminAddCategories")
    
    craftsmen_categories=db.relationship(
        "CraftsmanModel",back_populates="craftsmanHasCategories",lazy="dynamic")
    
    CategoryService=db.relationship(
        "ServiceModel",back_populates="category",lazy="dynamic")
    



