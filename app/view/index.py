# coding=utf-8

from __future__ import absolute_import
from app import app
from app.support import auth
from trex.flask import AuthBlueprint, render_html

blueprint = AuthBlueprint('index', __name__)


@blueprint.route('/', auth=auth.public)
@render_html()
def index():
    return {}

@blueprint.route('/sheet-test', auth=auth.public)
@render_html()
def sheet_test():
    return {}


app.register_blueprint(blueprint)
