from db import db

class WalletModel(db.Model):
    __tablename__="WalletModel"

    id = db.Column(db.Integer, primary_key=True)
    craftsman_id=db.Column(db.Integer,db.ForeignKey("CraftsmanModel.id",ondelete='CASCADE'),nullable=False)
    balance=db.Column(db.Float(precision=2),nullable=False)
    


