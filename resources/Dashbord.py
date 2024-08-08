from flask.views import MethodView
from flask import jsonify
from flask_smorest import Blueprint

from db import db



from models import CraftsmanModel,ClientModel,StoreModel


blp = Blueprint("Graphs", "dash ", description="Dashboard for admin all graphs data")
@blp.route("/Admin/Dashboard")
class DashboraderGraphs(MethodView):
    def get(self):
        Clients=ClientModel.query.count()
        pendingCraftsmen=CraftsmanModel.query.filter_by(Pending=True).count()
        approvedCraftsmen=CraftsmanModel.query.filter_by(Pending=False).count()
        total_craftsmen= pendingCraftsmen + approvedCraftsmen
        stores=StoreModel.query.count()
        # approvedPercentage=approvedCraftsmen / total_craftsmen
        # pendingpercentage=1-approvedPercentage

        return jsonify({
            "Clients": Clients,
            "pending craftsmen":pendingCraftsmen,
            # "pending percentage":pendingpercentage,
            "approved craftsmen":approvedCraftsmen,
            # "approved percentage":approvedPercentage,
            "total craftsmen":total_craftsmen,
            "Stores":stores
             }) 

