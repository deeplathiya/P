# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from sqlalchemy import Column, Integer, String, Float, Boolean

from project.models.init_db import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    orderId = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

class PaymentReturn(db.Model):
    __tablename__ = 'paymentreturns'

    orderId = Column(Integer, nullable=False)
    paymentId = Column(Integer, primary_key=True, nullable=False)
    status = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)