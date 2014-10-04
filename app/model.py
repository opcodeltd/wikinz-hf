# coding=utf-8

from __future__ import absolute_import
from app import app
from trex.support import quantum
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

class Table(Document):
    """
    Grid table of data
    """
    created = QuantumField(default=quantum.now)
    creator = ReferenceField('User')
    title = StringField()
    description = StringField()
    source = ReferenceField('Source') # This could be None if the source is another table or something
    data = DynamicField()


class Source(Document):
    """
    Source document, XLS or whatever
    """
    created = QuantumField(default=quantum.now)
    creator = ReferenceField('User')
    title = StringField()
    source = StringField()
    filename = StringField()
    file = ReferenceField('TrexUpload', required=True)

class Graph(Document):
    """
    Graph/Chart definition
    """
    created = QuantumField(default=quantum.now)
    creator = ReferenceField('User')
    title = StringField()
    description = StringField()
    table = ReferenceField('Table')
    # x and y axis selection?
