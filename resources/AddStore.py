from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db

from sqlalchemy.exc import SQLAlchemyError


from models import AdminModel,StoreModel
from Schemas import PlainAddStoreSchema,PlainAddItemSchema,PlainAddStoreSchema

blp = Blueprint("Add Stores", "stores", description="Admin add store")



@blp.route("/Admin/Store")
class AddStore(MethodView):
    @jwt_required()
    @blp.arguments(PlainAddStoreSchema)
    def post(self, Stores_data):

        admin_id=get_jwt_identity()
        if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role !="operational" ).first():
            abort(401,
                   message="Permission denied. Only operational admins can add stores."

                  )
        if StoreModel.query.filter(StoreModel.name == Stores_data["name"],
                                   StoreModel.location==Stores_data["location"]).first():
            
            abort(409,
                  message="The Store already exits")
            
        store=StoreModel(
                name=Stores_data["name"],
                location=Stores_data["location"],
                description=Stores_data["description"],
                phone=Stores_data["phone"],
                admin_id=admin_id
           
            )
        try:
            db.session.add(store)
            db.session.commit()
            
        except SQLAlchemyError as e:

            db.session.rollback()
            abort(500, message="Failed to add store")

        return {"message":"Store added successfully."},201
    

@blp.route("/Store/<int:store_id>/items")
class Storeitems(MethodView):
    @blp.response(200,PlainAddItemSchema(many=True))
    def get(self,store_id):
        store=StoreModel.query.filter_by(id=store_id).first()
        if not store :
            abort(404,message="Store not found.")
        return store.items.all()
    

@blp.route("/Admin/Store/<int:store_id>")
class deleteStore(MethodView):
    def delete(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store and all associated items have been deleted."}
    

@blp.route("/Stores/data")
class Storedata(MethodView):
    # @blp.response(200,PlainAddItemSchema(many=True))
    def get(self):
        # i get list of dictionries from the database [{name:value}]
        stores = StoreModel.query.all()

        # If no stores found, return 404
        if not stores:
            abort(404, message="No stores found.")

        # Prepare the data with item counts for each store
        stores_data = []
        for store in stores:# for each dict in the stores list
            store_data = PlainAddStoreSchema().dump(store)# this is a dict >> serialize the dict to deal with it first 

            # its like adding a column to the object coming from the database since you add a key to the dictionary called store_data
            store_data['items_count'] = store.items.count() # add a key to the store_data dict with the number of the items
            stores_data.append(store_data)# add this dic to the empty list called >> stores-data[] 

        # Return the response with all stores and their item counts
        return jsonify({"stores": stores_data}), 200

    