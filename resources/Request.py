# from flask import request, jsonify
# from flask.views import MethodView
# from flask_smorest import Blueprint, abort
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from db import db

# from sqlalchemy.exc import SQLAlchemyError

# from models import UserModel,ClientModel,OrderModel,ServiceModel,OrderServicesModel,CraftsmanModel,ClientLocationModel,CraftsmanLocationModel,LocationModel,RatingModel
# from Schemas import ServiceListSchema,CraftsmanSchema,ReturnlocationSchema,FilteredCraftsmen,orderServices,orderSchema,nestedorder,NewOrderSchema,OrderServicesOnlySchema,RequestedCraftsman,serialzed
# def avg_rating(craftsman_id):
#     """Calculates the average rating for a craftsman."""
#     ratings = RatingModel.query.filter_by(craftsman_id=craftsman_id).all()
#     if not ratings:
#         return None  # Handle no ratings case gracefully
#     avg = sum(rating.rating for rating in ratings) / len(ratings)
#     return round(avg , 2)
# def calculate_order_total(order_id):
#     # Get the order with the specified order_id
#     order = OrderModel.query.get(order_id)
    
#     # Initialize the total price
#     total_price = 0
    
#     # Iterate over the services associated with the order
#     for service in order.order_services:
#         total_price += service.price
    
#     return total_price

# blp = Blueprint("Clients request", "Clients make request",
#                 description="Client make request")


# @blp.route("/request")
# class Request(MethodView):
#     @jwt_required()
#     @blp.arguments(ServiceListSchema)
#     def post(self,service_data):
#         # Get the client identiy
#         client_id=get_jwt_identity()
#         """
#         #Get the client Location 
#         # client_location=ClientLocationModel.query.filter_by(client_id=client_id).first()
#         # Get the client city to get all the craftsmen in this city
#         # city=client_location.city
#         # Make an order with the client id to fill it with the services
#         """
#         order=OrderModel(
#             client_id=client_id
#         )

#         db.session.add(order)
        
#         try:
#             # Loop through each service in the list 
#             for service in service_data["services"]:
#                 # Check if each service is available
#                 new_service=ServiceModel.query.filter_by(name=service).first()
#                 if not new_service : # If not found:
#                     abort(404 , message="service not found")
#                 # if the service is found :
#                 # fill all the services provided by the client to the order he just made
#                 add_service=OrderServicesModel(
#                     order_id=order.order_id,
#                     service_id=new_service.id)
                
#                 db.session.add(add_service)

         
#         except SQLAlchemyError:
#             abort(500,message='internal server error')

#         db.session.commit()    

#         """
#         # craftsmen = CraftsmanModel.query.join(CraftsmanLocationModel).join(LocationModel).filter(
#                 #     LocationModel.name == city,CraftsmanModel.is_available==True
#                 # ).all()
#                 # serialized_craftsman = CraftsmanSchema(many=True).dump(craftsmen)  
#         """
#         return jsonify(
#             {"message": "Order has been added.","Order number ":order.order_id})
    
# @blp.route("/craftsmenForOrder")
# class RequestCraftsmen(MethodView):
#     # @jwt_required()
#     @blp.arguments(FilteredCraftsmen)
#     def get(self,order_data):

#         area=LocationModel.query.filter(LocationModel.name==order_data["city"]).first()
#         if not area :
#             return jsonify({"Message":"We do not operate in " + order_data["city"] + " yet!"}),200
#            #abort(200,message="We do not operate in " + order_data["city"] + " yet!")

#         services=OrderServicesModel.query.filter(OrderServicesModel.order_id==order_data["order_id"]).all()
#         serialized_service=orderServices(many=True).dump(services)

#          # Get the categories of the services in the order
#         service_ids = [service.service_id for service in services]
#         service_categories = ServiceModel.query.filter(ServiceModel.id.in_(service_ids)).all()
#         category_ids = {service.category_id for service in service_categories}

#         craftsmen = CraftsmanModel.query.join(CraftsmanLocationModel).join(LocationModel).filter(
#             LocationModel.name == order_data["city"],
#             CraftsmanModel.is_available==True,
#             CraftsmanModel.Pending==False,
#             CraftsmanModel.category_id.in_(category_ids)
#         ).all()

#         if not craftsmen:
#             return jsonify({"Message":"Sorry but it seems like no craftsmen are available in the moment, Please try again in a while."}),200
#             #abort(404,Message="Sorry but it seems like no craftsmen are available in the moment, Please try again in a while.")

#         serialized_craftsman = RequestedCraftsman(many=True).dump(craftsmen)

#         for craftsman in serialized_craftsman:
#              craftsman['rating'] = avg_rating(craftsman['id'])
#              if craftsman['rating'] is None or craftsman['rating'] == 0:
#                     craftsman['rating'] = 1
#              if craftsman["rating"] >= 0 and craftsman["rating"] < 2:
#                 craftsman['fair'] = calculate_order_total(order_data["order_id"]) * 0.85
#              elif craftsman["rating"] >= 2 and craftsman["rating"] < 3:
#                 craftsman['fair'] = calculate_order_total(order_data["order_id"]) * 0.90
#              elif craftsman["rating"] >= 3 and craftsman["rating"] < 4:
#                 craftsman['fair'] = calculate_order_total(order_data["order_id"]) * 1.00
#              elif craftsman["rating"] >= 4 and craftsman["rating"] <= 5:
#                 craftsman['fair'] = calculate_order_total(order_data["order_id"]) * 1.10
       
#         order_total=calculate_order_total(order_data["order_id"])
#         return jsonify({"Avaialble craftsmen for your order ": serialized_craftsman,
#                         "services":serialized_service,"Total of order":order_total})
        
# @blp.route("/SelectCraftsman/<int:order_id>/<int:craftsman_id>")
# class selectCraftsman(MethodView):
#     def post(self,order_id,craftsman_id):
#         craftsman=CraftsmanModel.query.filter(CraftsmanModel.id==craftsman_id).first()
#         if not craftsman:
#             abort(404,message=" Craftsman not found")
#         if craftsman.Pending==True:
#             return{"Message":"You can not assign this craftsman to the order, he is still under supervision"}
#         order=OrderModel.query.filter(OrderModel.order_id==order_id).first()
#         if not order :
#             abort(404,Message="Order not found.")

#         order.craftsman_id=craftsman.id
#         craftsman.is_available=False        
#         db.session.commit()
#         return jsonify({"Message":"Done: the order now has a craftsman , the craftsman is not available anymore till the request has an end "})
    
# @blp.route("/CloseRequest/<int:order_id>")
# class CloseRequest(MethodView):
#     def post(self,order_id):
#         order=OrderModel.query.filter_by(order_id=order_id).first()
#         if not order :
#             abort(404,message="Order not found check the order number .")
#         if order.done==True:
#             return{"Message":"The order is already closed"}
#         if not order.craftsman_id:
#             return{"Message":"The order has no craftsman we will delete it inshaa'allah"}

#         order.done=True
#         craftsman_id=order.craftsman_id
#         craftsman=CraftsmanModel.query.filter_by(id=craftsman_id).first()
#         craftsman.is_available=True
#         craftsman.completed_orders = craftsman.completed_orders + 1
#         db.session.commit()
#         return jsonify({"Message":"Thanks for using fixr app","Note":"Now craftsmen is avaialble again"}),200


# @blp.route("/MyOrders")
# class myOrders(MethodView):
#     @jwt_required()
#     def get (self):
#         user_id=get_jwt_identity()
#         user=UserModel.query.filter_by(id=user_id).first()
#         if user.user_type =="client":
#             orders=OrderModel.query.filter(OrderModel.client_id==user.id).all()
#             if orders:
#                 serialized_orders=NewOrderSchema(many=True).dump(orders)
#                 return jsonify({"My orders": serialized_orders})
#             return jsonify({"Message":"No orders for this client yet!"})
        
#         elif user.user_type =="craftsman":
#             orders=OrderModel.query.filter(OrderModel.client_id==user.id).all()
#             if orders:
#                 serialized_orders=NewOrderSchema(many=True).dump(orders)
#                 return jsonify({"My orders": serialized_orders})
#             return jsonify({"Message":"No orders for this Craftsman yet!"})
        
#         else:
#             return jsonify({"Message":"User not found."})



# @blp.route("/OrderServices/<int:order_id>")
# class see(MethodView):
#     def get(self,order_id):
#         order=OrderModel.query.filter_by(order_id=order_id).first()
#         if not order :
#             abort(404,message="Order not found check the order number .")

#         result=OrderServicesOnlySchema().dump(order)
#         return jsonify({"Message : services":result})
    

# # @blp.route("/test/<int:craftsman_id>")
# # class test(MethodView):
# #     def get(self,craftsman_id):
    
# #         rating=avg_rating(craftsman_id)
# #         if not rating:
# #             abort(404,message="mfish")
# #         return {"Rate":rating}

# @blp.route("/test/<int:order_id>")
# class test(MethodView):
#     def get(self,order_id):
    
#         price=calculate_order_total(order_id)
#         if not price:
#             abort(404,message="mfish")
#         return {"price":price}