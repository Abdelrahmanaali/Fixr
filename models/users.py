from db import db


class UserModel(db.Model):
    __tablename__ = "UserModel"
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(255), unique=False, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    Email = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=True)
    user_type = db.Column(db.String(255), nullable=False)

    messages = db.relationship(
        "MessageModel", back_populates="user", lazy="dynamic")
    



    user_admin = db.relationship("AdminModel", back_populates="admin_user", cascade="all, delete-orphan", uselist=False)

    # Relationship with ClientModel
    user_client = db.relationship("ClientModel", back_populates="client_user", cascade="all, delete-orphan", uselist=False)

    # Relationship with CraftsmanModel
    user_craftsman = db.relationship("CraftsmanModel", back_populates="craftsman_user", cascade="all, delete-orphan", uselist=False)


class AdminModel(UserModel):
    __tablename__ = "AdminModel"
    id = db.Column(db.Integer, db.ForeignKey("UserModel.id"),primary_key=True)
    Role = db.Column(db.String(255), unique=False, nullable=False)

    adminAddCategories = db.relationship(
        "CategoryModel", back_populates="admin_categories", lazy="dynamic")

    adminAddLocations = db.relationship(
        "LocationModel", back_populates="admin_locations", lazy="dynamic")

    adminAddStores = db.relationship(
        "StoreModel", back_populates="admin_stores", lazy="dynamic")
    
    adminAddService=db.relationship(
        "ServiceModel",back_populates="service",lazy="dynamic"
    )

    admin_user = db.relationship("UserModel", back_populates="user_admin")


class ClientModel(UserModel):
    __tablename__ = "ClientModel"
    id = db.Column(db.Integer, db.ForeignKey("UserModel.id",ondelete='CASCADE'), primary_key=True)
    profile_pic = db.Column(db.String(255), nullable=True)


    # clientLocation = db.relationship(
        # "ClientLocationModel", back_populates="selctedLocation", lazy="dynamic",cascade="all, delete-orphan")
    
    client_user = db.relationship("UserModel", back_populates="user_client")

    order=db.relationship("OrderModel",back_populates="client_order",lazy="dynamic")

    # rate=db.relationship("CraftsmanModel",back_populates="rating",secondary="RatingModel")

    # payments=db.relationship("PaymentModel",back_populates="payment",lazy="dynamic")

class CraftsmanModel(UserModel):
    __tablename__ = "CraftsmanModel"
    id = db.Column(db.Integer, db.ForeignKey("UserModel.id",ondelete='CASCADE'), primary_key=True)
    is_available = db.Column(db.Boolean, nullable=False,
                             default=True)  # Column definition
    
    front_image = db.Column(db.String(255), nullable=True)
    back_image = db.Column(db.String(255), nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    completed_orders=db.Column(db.Integer, nullable=True ,default=0)

    Pending=db.Column(db.Boolean, nullable=False,default=True)

    category_id = db.Column(db.Integer, db.ForeignKey(
        "CategoryModel.id"), nullable=False)



    craftsmanHasCategories = db.relationship(
        "CategoryModel"
        , back_populates="craftsmen_categories"
        )
    
    operatingLocation=db.relationship(
        "LocationModel"
        ,back_populates="craftsmanLocation"
        ,secondary="CraftsmanLocationModel"
        
    )

    craftsman_user = db.relationship(
        "UserModel", back_populates="user_craftsman")
    
    orders=db.relationship(
        "OrderModel",back_populates="craftsman_order")
    
    # rating=db.relationship("ClientModel",back_populates="rate",secondary="RatingModel")