# coding=utf-8

from __future__ import absolute_import
import json
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
    """
    Data should look like this:

    { cols: [ { title: { value: 'blah' }, values: [ { 'value': 0 }, {'value': 10} ] } ] }
    """
    data = DynamicField()

    def as_rows(self):
        rows = []
        for x in range(0, len(self.data['cols'][0]['values'])):
            row = []
            for y in range(0, len(self.data['cols'])):
                print x,y,self.data['cols']

                row.append(self.data['cols'][y]['values'][x])
            rows.append(row)
        return rows


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

    If axis is None, we use titles for the x axis, otherwise titles become labels for the series
    """
    created = QuantumField(default=quantum.now)
    creator = ReferenceField('User')
    title = StringField()
    type = StringField()
    description = StringField()
    table = ReferenceField('Table')
    axis = IntField()
    cols = ListField(IntField())

    def as_chartable(self):
        out = {}
        out['source'] = {'title': self.table.title}
        if self.axis >= 0:
            categories = [c['value'] for c in self.table.data['cols'][self.axis]['values']]
        else:
            categories = [c['title']['value'] for c in self.table.data['cols']]

        out['axis'] = {
            'categories': categories
        }

        out['series'] = []

        for index in self.cols:
            out['series'].append({
                'title': self.table.data['cols'][index]['title']['value'],
                'data': [c['value'] for c in self.table.data['cols'][index]['values']]
            })

        return json.dumps(out)

