import os
import pytest
import unittest

from service import app, db, CurrencyRate


@pytest.fixture
def client():
    ## Setup for each test ##
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://me:pw@testdb:5432/mytestdb'

    client = app.test_client()
    
    with app.app_context():
        db.create_all()

    yield client

    ## Teardown for each test ##
    with app.app_context():
        db.session.close()
        db.drop_all()


def test_ingest_created(client):
    resp = client.get('/ingest')
    assert resp.status_code == 201

    eur_curr = CurrencyRate.query.filter_by(currency="EUR").first()
    # As it's the base currency
    assert eur_curr.rate == 1


def test_ingest_200(client):
    resp1 = client.get('/ingest')
    resp2 = client.get('/ingest')

    assert resp2.status_code == 200
