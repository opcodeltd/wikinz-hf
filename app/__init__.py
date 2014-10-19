from __future__ import absolute_import

from trex.flask import Flask
from trex.support.audit import TrexAudit

app = Flask(__name__)
TrexAudit(app)

from . import view
import trex.support.blueprint_auth
import trex.support.blueprint_user_management
import trex.support.blueprint_audit_log
import trex.support.blueprint_templates
