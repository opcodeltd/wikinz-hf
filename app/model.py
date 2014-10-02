# coding=utf-8

from __future__ import absolute_import
from app import app
from mongoengine import *
from trex.support.model import BaseDocument as Document, BaseAudit, BaseIdentity, BaseUser
from trex.support.mongoengine import QuantumField, LowerCaseEmailField, QuantumDateField

class Audit(BaseAudit):
    pass

class Identity(BaseIdentity):
    pass

class User(BaseUser):
    pass
