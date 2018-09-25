import datetime
import os

import requests

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


db_pw = os.environ.get('PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://me:{}@db:5432/mydb'.format(db_pw)
db = SQLAlchemy(app)


# As app grows we'd move this to a models file
class CurrencyRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    # Currency with relative value of 1
    base = db.Column(db.String(64), nullable=False)
    currency = db.Column(db.String(6), nullable=False)
    rate = db.Column(db.Integer)

    def __repr__(self):
        return '<CurrencyRate {} on {} ({} base currency)>'.format(
                self.currency, self.date, self.base)


#db.drop_all()
# Idempotent
db.create_all()


@app.route("/ingest")
def ingest():
    api_key = os.environ.get('API_KEY')
    print(api_key)
    fixer_url = "http://data.fixer.io/api/latest?access_key={}".format(api_key)
    req = requests.get(fixer_url)
    data = req.json()

    updates = 0
    for curr, rate in data["rates"].items():
        date = datetime.datetime.strptime(data["date"], '%Y-%m-%d').date()
        currency_rate = CurrencyRate.query.filter_by(date=date, 
            base=data["base"], currency=curr).first()
        if not currency_rate:
            currency_rate = CurrencyRate(date=data["date"], 
                base=data["base"], currency=curr, rate=rate)        
            db.session.add(currency_rate)
            updates += 1

    db.session.commit()
    crs = CurrencyRate.query.all()
    if updates: 
        return Response(
            "Stored rates (with currency base '{}') for {} for {} currencies".format(
            data["base"], data["date"], updates), status=201)
    else: 
        return Response(
            "Rates (with currency base '{}') already stored for {}".format(
            data["base"], data["date"]), status=200)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
