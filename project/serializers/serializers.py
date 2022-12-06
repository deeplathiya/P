from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

from project.models.models import Payment, PaymentReturn


class PaymentSchema(SQLAlchemySchema):
    class Meta:
        model = Payment
        fields = ('id', 'orderId', 'amount', 'status')

class PaymentReturnSchema(SQLAlchemySchema):
    class Meta:
        model = PaymentReturn
        fields = ('orderId', 'paymentId', 'status', 'success')
