from __future__ import absolute_import

from trex.flask import Flask

app = Flask(__name__)

from flask.ext.sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = app.settings.get('postgresql', 'url')
app.psql = SQLAlchemy(app)
app.query = app.psql.engine.execute

from . import view
import trex.support.blueprint_auth
import trex.support.blueprint_user_management
import trex.support.blueprint_audit_log
import trex.support.blueprint_templates
