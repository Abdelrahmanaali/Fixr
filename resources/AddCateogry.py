from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db



from models import CategoryModel,AdminModel
from Schemas import PlainAddCategorySchema , AddcategorySchema

blp = Blueprint("Add category", "categories", description="Admin add categories")



@blp.route("/Admin/Category")
class AddCategory(MethodView):
    @jwt_required()
    @blp.arguments(PlainAddCategorySchema)
    def post(self, Category_data):

        admin_id=get_jwt_identity()
        if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role !="operational" ).first():
            abort(401,
                   message="Permission denied. Only operational admins can add categories."

                  )
        if CategoryModel.query.filter(CategoryModel.name == Category_data["name"]).first():
            abort(409,
                  message="this category already exits")
            
        category=CategoryModel(
                name=Category_data["name"],
                details=Category_data["details"],
                admin_id=admin_id
           
            )
        db.session.add(category)
        db.session.commit()
        return {"message":"category added successfully."},201
   



    @blp.response(201,AddcategorySchema(many=True))
    def get(self):
        Categories=CategoryModel.query.all()
        if not Categories:
            return jsonify({"Messages":"No categories"})
        return Categories





@blp.route("/Admin/Category/<int:category_id>")
class DeleteItem(MethodView):
    def delete(self,category_id):
        category=CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return{"Message":"category deleted"},200