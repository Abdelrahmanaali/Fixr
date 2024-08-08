from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from sqlalchemy.sql import func


from models import OrderModel,RatingModel,ServiceModel,OrderServicesModel,ClientModel,CraftsmanModel
from Schemas import orderSchema
def avg_rating(craftsman_id):
    """Calculates the average rating for a craftsman."""
    avg_rating = db.session.query(
        func.avg(RatingModel.rating)
    ).join(OrderModel, OrderModel.order_id == RatingModel.order_id).filter(
        OrderModel.craftsman_id == craftsman_id
    ).scalar()

    if avg_rating is None:
        return None

    return round(avg_rating, 2)

def Craftsman_feedback(craftsman_id):
    feedbacks = db.session.query(RatingModel).join(
        OrderModel, OrderModel.order_id == RatingModel.order_id
    ).filter(
        OrderModel.craftsman_id == craftsman_id,
        RatingModel.feedback.isnot(None),
        RatingModel.rating.isnot(None),
        RatingModel.feedback != '',
        RatingModel.rating != 0
    ).all()# Filter records with feedback and rating
    if not feedbacks:
        return None
    return feedbacks

def calculate_order_total(order_id):
    # Get the order with the specified order_id
    order = OrderModel.query.get(order_id) 
    # Initialize the total price
    total_price = 0 
    # Iterate over the services associated with the order
    for service in order.order_services:
        total_price += service.price
    return total_price

def Calculate_rate(rate,order_total):
    # rate=avg_rating(craftsman_id)
    if rate is None or rate == 0:
        rate = 1 
   
    if rate > 0  and rate < 2:
        new_total=order_total * 0.90
    elif rate >= 2 and rate < 3:
        new_total=order_total*0.95
    elif rate >=3 and rate < 4:
        new_total=order_total * 1
    elif rate >= 4 and rate <=5:
        new_total=order_total * 1.1


    return round(new_total , 2 )   

def order_summary(order_id):
        
        order=OrderModel.query.filter_by(order_id=order_id).first()
        if not order :
         return jsonify({"Message":"Order not found "}),404
        if order.craftsman_id == None:
            return{"message":"cannot complete"}
        if order.is_finished == False:
           return jsonify({"Message":"Order not closed yet "}),200
           
        client=ClientModel.query.filter_by(id=order.client_id).first()
        craftsman=CraftsmanModel.query.filter_by(id=order.craftsman_id).first()
      
        serialized_order=orderSchema().dump(order)
        serialized_order['Client_name']=client.name
        serialized_order['craftsman_name']=craftsman.name
        return serialized_order






# def avg_rating(craftsman_id):
#     """Calculates the average rating for a craftsman."""
#     ratings = RatingModel.query.filter_by(craftsman_id=craftsman_id).all()
#     if not ratings:
#         return None  # Handle no ratings case gracefully
#     avg = sum(rating.rating for rating in ratings) / len(ratings)
#     return round(avg , 2)