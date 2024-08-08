from flask.views import MethodView
from flask import jsonify,request
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required , get_jwt_identity
from db import db
from sqlalchemy import exists


from models import ServiceModel , CategoryModel ,AdminModel
from Schemas import AddServiceSchema,ServicesWithCategory,PlainServiceSchema

blp = Blueprint("Add Services", "service", description="Admin add services")
# Add service
@blp.route("/Admin/Service")
class AddService(MethodView):
    @blp.arguments(AddServiceSchema)
    @blp.response(201,ServicesWithCategory)
    @jwt_required()
    def post(self,service_data):

        admin_id=get_jwt_identity()

        if AdminModel.query.filter(AdminModel.id==admin_id , AdminModel.Role != "operational" ).first():
            abort(401,
                   message="Permission denied. Only operational admins can add services."
                  )
            
        if ServiceModel.query.filter_by(name=service_data["name"]).first():
            abort(409,
                  message="This service already exsits")
        
          
        category=CategoryModel.query.filter_by(name=service_data["category"]).first()
        if not category:
            abort(404,
                  message="category not found.")
        
            
        service=ServiceModel(
            name=service_data["name"],
            price=service_data["price"],
            category_id=category.id,
            admin_id=admin_id
        )

        db.session.add(service)
        db.session.commit()
        return service
        
        

    # Return all services
    @blp.response(201,ServicesWithCategory(many=True))
    def get(self):
        services=ServiceModel.query.all()
        return services
    


@blp.route("/Admin/Service/<int:service_id>")
class deleteService(MethodView):
    def delete(self,service_id):
        service=ServiceModel.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return{"Message":"Service deleted."},200


# Filter services by the category id 
@blp.route("/Admin/<int:category_id>")
class ServicesInCategory(MethodView):
    @blp.response(201,PlainServiceSchema(many=True))
    def get(self,category_id):
        services=ServiceModel.query.filter(ServiceModel.category_id==category_id).all()
        return services