# coding=utf-8

from __future__ import absolute_import
from app import app
from app.support import auth
from trex.flask import AuthBlueprint, render_html
from trex.support import wtf, quantum
from flask import abort, g, redirect, url_for
import json


blueprint = AuthBlueprint('index', __name__)


@blueprint.route('/', auth=auth.public)
@render_html()
def index():
    return {}

@blueprint.route('/sheet-test', auth=auth.public)
@render_html()
def sheet_test():
    return {}

@blueprint.route('/import-test', auth=auth.public)
@render_html()
def import_test():
    return {}

@blueprint.route('/import-begin', auth=auth.public, methods=['GET','POST'])
@render_html()
def import_begin():
    class Form(wtf.Form):
        json_file = wtf.FileField(
            'JSON file',
            [wtf.validators.Required()],
            allow_clear = False,
        )

    form = Form()

    if form.validate_on_submit():
        open('import-in-progress.json','w').write(form.json_file.data)
        return redirect(url_for('index.import_review'))

    return dict(form=form)

@blueprint.route('/import-review', auth=auth.public, methods=['GET', 'POST'])
@render_html()
def import_review():
    data = json.load(open('import-in-progress.json','r'))
    return {}

app.register_blueprint(blueprint)
