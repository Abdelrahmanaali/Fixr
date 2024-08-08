import os

from flask import Flask 
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import pytz

from flask_mail import Mail
mail = Mail()

from db import db
import models

import cloudinary
from cloudinary.uploader import upload

cloudinary.config(
    cloud_name="dmdrp6inr",
    api_key="816263894333586",
    api_secret="b1v_MAVriadAz9Z_SiZTRoVwnVE"
)

from resources.AdminRegistration import blp as AdminBlueprint
from resources.ClientRegistration import blp as ClientBlueprint
from resources.CraftsmanRegistration import blp as CraftsmanBlueprint
from resources.Login import blp as LoginBlueprint
from resources.Addoperatinglocation import blp as OperatingLocationsBlueprint
from resources.ComplainMessage import blp as ClientMessageBlueprint
from resources.AddCateogry import blp as CategoryBlueprint
from resources.AddStore import blp as StoreBlueprint
from resources.AddItems import blp as AddItemBlueprint
from resources.ClientProfile import blp as ClientProfileBluePrint
from resources.CraftsmanLocations import blp as CraftsmanLocations
from resources.CraftsmanImage import blp as UploadImage
from resources.PendingCraftsmen import blp as Pending
from resources.generateCoupons import blp as CoupounsBluePrint
from resources.AddServices import blp as AddServicesBluePrint
from resources.Dashbord import blp as DashboradBlueprint
from resources.Profiles import blp as Userprofiles
from resources.CraftsmanBalance import blp as balanceBluePrint
# from resources.Request import blp as requestblueprint
#--------------------------request----------------------
from resources.MakeRequest import blp as MakeRequestBlueprint
from resources.CraftsmenListForRequest import blp as CraftsmanListBlueprint
from resources.SelectCraftsman import blp as SelectCraftsmanBlueprint
from resources.CloseRequest import blp as CloseRequestBlueprint
from resources.Myorders import blp as MyordersBlueprint
from resources.OrderServices import blp as OrderServicesBlueprint
from resources.CraftsmanReviews import blp as CraftsmanReviewsBlueprint
from resources.Payment import blp as CheckoutBluePrint









def create_app(db_url=None):

    app= Flask(__name__)
    load_dotenv()




    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')




    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "FIXR REST API"  # for the documentation
    app.config["API_VERSION"] = "v1"  # for the documentation
    app.config["OPENAPI_VERSION"] = "3.0.3"    # standard
    app.config["OPENAPI_URL_PREFIX"] = "/"     #
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



    db.init_app(app)    
    mail.init_app(app)
    migrate=Migrate(app,db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"]="Abdulrahman"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 5000  # Set expiration time to 1 hour (3600 seconds)
    app.config['TIMEZONE'] = pytz.timezone('Africa/Cairo')


   


    jwt = JWTManager(app)

    # @jwt.expired_token_loader
    # def expired_token_loader(jwt_header,jwt_payload):
    #     return jsonify({"Error":"Your login session has been expired , please reloign"})

    # @jwt.unauthorized_loader
    # def unauthorized_callback(callback):
    #     return jsonify({"Error": "Authorization header missing or invalid"}), 401


    api.register_blueprint(AdminBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(ClientBlueprint)
    api.register_blueprint(CraftsmanBlueprint)
    api.register_blueprint(OperatingLocationsBlueprint)
    api.register_blueprint(ClientMessageBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(AddItemBlueprint)
    api.register_blueprint(ClientProfileBluePrint)
    api.register_blueprint(CraftsmanLocations)
    api.register_blueprint(UploadImage)
    api.register_blueprint(Pending)
    api.register_blueprint(CoupounsBluePrint)
    api.register_blueprint(AddServicesBluePrint)
    api.register_blueprint(DashboradBlueprint)
    api.register_blueprint(Userprofiles)
    api.register_blueprint(balanceBluePrint)
    # api.register_blueprint(requestblueprint)
#----------------- request ------------------
    api.register_blueprint(MakeRequestBlueprint)
    api.register_blueprint(CraftsmanListBlueprint)
    api.register_blueprint(SelectCraftsmanBlueprint)
    api.register_blueprint(CloseRequestBlueprint)
    api.register_blueprint(MyordersBlueprint)
    api.register_blueprint(OrderServicesBlueprint)
    api.register_blueprint(CraftsmanReviewsBlueprint)
    api.register_blueprint(CheckoutBluePrint)

    return app

