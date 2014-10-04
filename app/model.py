# coding=utf-8

from __future__ import absolute_import
from app import app
from mongoengine import *
from trex.support.model import BaseDocument as Document, BaseAudit, BaseIdentity, BaseUser
from trex.support.mongoengine import QuantumField, LowerCaseEmailField, QuantumDateField
from trex.support import token

class Audit(BaseAudit):
    pass

class Identity(BaseIdentity):
    pass

class User(BaseUser):
    pass


class Chartable(Document):
    token = StringField(required=True, default=token.create_url_token)
    name  = StringField(required=True)

class ChartableColumn(Document):
    meta = dict(allow_inheritance=True)

    chartable = ReferenceField('Chartable', required=True)
    name = StringField(required=True)

class ChartableColumnDate(ChartableColumn):
    data = ListField(QuantumDateField(required=True))

class ChartableColumnDateTime(ChartableColumn):
    data = ListField(QuantumField(required=True))

class ChartableColumnNumber(ChartableColumn):
    data = ListField(IntField(required=True))

class ChartableColumnString(ChartableColumn):
    data = ListField(StringField(required=True))
