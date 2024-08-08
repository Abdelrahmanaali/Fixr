from flask.views import MethodView
from flask import jsonify,request
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db
from sqlalchemy import exists
from cloudinary.uploader import upload

from models import AdminModel,ItemModel,StoreModel
from Schemas import PlainAddItemSchema,ItemsInStoreSchema,SpeceficItemSchema,ReturnSpeceficItemSchema

blp = Blueprint("Add Items", "items", description="Admin add items")
""""
1-Post(/Admin/Item)>>add items
2-get(/Admin/Item)>>get all items
3-get ("/Admin/Item/Name")>> get one item and all stores 
"""


@blp.route("/Admin/Item")
class AddItem(MethodView):
    @jwt_required()
    @blp.arguments(PlainAddItemSchema)

    # Create an item
    def post(self, Item_data):

        admin_id=get_jwt_identity()

        if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role != "operational" ).first():
            abort(401,
                   message="Permission denied. Only operational admins can add items."
                  )
            
        store=StoreModel.query.filter(StoreModel.name==Item_data["store_name"]).first()

        if not store :
            abort(404,message="store not found")


        item_exists = db.session.query(exists().where(
            ItemModel.name==Item_data["name"],
            ItemModel.price==Item_data["price"],
            ItemModel.store_id==store.id
        )).scalar()

        if item_exists:
            abort(409, message="This item with this price exsits already.")


        item=ItemModel(
                    name=Item_data["name"],
                    price=float(Item_data["price"]),
                    quantity=int(Item_data["quantity"]),
                    store_id=store.id

                )
        
        db.session.add(item)
        db.session.commit()
        return {"message":"Item added successfully."},201
    
    #Retrive all items
    @jwt_required()
    @blp.response(201,ItemsInStoreSchema(many=True))
    def get(self):

        admin_id=get_jwt_identity()

        if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role != "operational" ).first():
            abort(401,
                   message="Permission denied. Only operational admins can add stores."
                  )
            
        return ItemModel.query.all()
    
# Search item by name 
@blp.route("/Admin/Item/Name")
class CertainItem(MethodView):
    @blp.arguments(SpeceficItemSchema)
    @blp.response(200,PlainAddItemSchema)
    def get(self, name):
        item = ItemModel.query.filter(ItemModel.name==name["name"]).first()
        if not item:
            abort(404, message="Item not found")  # Raise 404 if item not found
        return item


# Delete item by id 
@blp.route("/Admin/Item/<int:item_id>")
class DeleteItem(MethodView):
    def delete(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return{"Message":"Item deleted"},200


# Upload an image to an item
@blp.route("/Admin/Items/<int:item_id>/image")
class itemImage(MethodView):
    # @jwt_required()
    def put(self,item_id):
        # admin_id=get_jwt_identity()
        # if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role != "operational" ).first():
        #     abort(401,
        #            message="Permission denied. Only operational admins can add stores."
        #           )
        item=ItemModel.query.get(item_id)
        if not item:
            abort(404,
                  message="Item not found.")

        item_image=request.files["image"]

        if not item_image :
            abort(404,message="No files were uploaded")

        item_result=upload(item_image)

        item_image_url=item_result["secure_url"]

        item.image=item_image_url

        db.session.commit()
        return{"Url":item_image_url}
        