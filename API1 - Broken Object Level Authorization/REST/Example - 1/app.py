from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
path = Path(__file__)

ERROR = {"error": "An error occured."}


class Shop(db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    monthly_revenue = db.Column(db.Integer, nullable=False)
    annual_revenue = db.Column(db.Integer, nullable=False)
    average_revenue = db.Column(db.Integer, nullable=False)


app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f"sqlite:///{path.parent}/db.sqlite")
db.init_app(app)

with app.app_context():
    db.create_all()



@app.get("/shops")
def get_shops():
    try:
        return _get_shops()
    except:
        return ERROR
    


@app.get("/shops/<string:shop_name>/revenue_data.json")
def get_revenue(shop_name):
    try:
        return _get_revenue()
    except Exception as e:
        return ERROR


def _get_shops():
    shop_list = []
    for shop in Shop.query.all():
        shop_list.append({
            "name": shop.name
        })

    return shop_list


def _get_revenue(shop_name):
    shop = Shop.query.filter_by(name=shop_name).first()

    if shop:
        return {
            "monthly_revenue": shop.monthly_revenue,
            "annual_revenue": shop.annual_revenue,
            "average_revenue": shop.average_revenue
            }
    else:
        return []
