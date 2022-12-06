from datetime import datetime
from typing import Tuple

import connexion
from flask import jsonify
from sqlalchemy.orm import joinedload

from project.models.init_db import db
from project.models.models import Payment, PaymentReturn
from project.serializers.serializers import PaymentSchema, PaymentReturnSchema

import random, json, requests, time
from project.worker.task import pay

def post() -> dict:
    if connexion.request.is_json:
        data = connexion.request.get_json()
        payment = Payment(orderId = data["orderId"], amount = data["amount"], status = data["status"])
        db.session.add(payment)
        db.session.commit()
        payment = Payment.query.filter_by(orderId = data["orderId"]).first()
        # success_status = bool(random.randint(0,1))
        pay.delay(payment.id, payment.amount)

        while True:
            payment = Payment.query.filter_by(orderId = data["orderId"]).first()
            if payment.status == "success" or payment.status == "failed":
                break
            time.sleep(0.1)

        if payment.status == "success":
            paymentReturn = PaymentReturn(orderId = data["orderId"], paymentId = payment.id, status = "ordered", success = True)
            success_status = True
        else:
            paymentReturn = PaymentReturn(orderId = data["orderId"], paymentId = payment.id, status = "ordered", success = False)
            success_status = False

        # Calling the Put API of the order microservice
        url = "http://localhost"
        data = {'orderId': data["orderId"], 'paymentId': payment.id, 'status': 'ordered', 'success': success_status}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.put(url, data=json.dumps(data), headers=headers)

        return jsonify(PaymentReturnSchema().dump(paymentReturn))

    return jsonify({})

def put() -> dict:
    if connexion.request.is_json:
        data = connexion.request.get_json()
        payment = Payment.query.filter_by(id = data["id"]).first()
        if data["stat"] == 0:
            payment.status = "failed"
        else:
            payment.status = "success"

        return jsonify(PaymentSchema.dump(payment))

    return jsonify({})