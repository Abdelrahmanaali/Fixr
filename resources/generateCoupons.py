from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db
from datetime import datetime,timedelta

from pytz import timezone


import string
import random
from models import StoreModel ,CouponModel
from Schemas import CouponSchema





blp = Blueprint("Generate coupons", "coupons", description="Admin generate coupons inside a store")

egypt_tz = timezone('Africa/Cairo')


@blp.route("/Admin/Coupon/<string:store_name>")
class GenerateCoupon(MethodView):
    def get(self, store_name):
        # Find the store by name 
        store = StoreModel.query.filter_by(name=store_name).first()
        if not store:
            abort(404, message="Store not found")  # Handle missing store

        # Generate coupon code 
        random_chars = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(4))
        coupon_code = f"{store_name.upper()}{random_chars}"

        # Capture current time and set expiration date 
        current_time = datetime.now(egypt_tz)
        expiration_days = 7 # Explicitly define expiration days
        expiration_date = current_time + timedelta(days=expiration_days)

        # Create and save coupon to database
        new_coupon = CouponModel(
            store_id=store.id,
            code=coupon_code,
            value=10,  # Assuming a fixed value
            date_created=current_time.astimezone(egypt_tz),
            exp_date=expiration_date.astimezone(egypt_tz),
        )
        db.session.add(new_coupon)
        db.session.commit()

        # Format dates for response (DD/MM/YY)
        created_at_formatted = current_time.strftime("%d/%m/%Y")
        expires_at_formatted = expiration_date.strftime("%d/%m/%Y")

        return jsonify({
            "store": store_name.upper(),
            "coupon_code": coupon_code,
            "created_at": created_at_formatted,
            "expires_at": expires_at_formatted,
        })
    




@blp.route("/Admin/AllCoupons/<string:store_name>")
class Allcoupons(MethodView):
    @blp.response(201,CouponSchema(many=True))
    def get(self,store_name):
        store=StoreModel.query.filter_by(name=store_name).first()
        if not store :
            abort(404,
                  message="store not found!")
            
            
        coupons = store.coupon.all()
        # coupons_count=store.coupon.count()


        return coupons 