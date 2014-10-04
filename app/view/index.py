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
        form.json_file.data.to_file('import-in-progress.json')
        return redirect(url_for('index.import_review'))

    return dict(form=form)

@blueprint.route('/import-review', auth=auth.public, methods=['GET', 'POST'])
@render_html()
def import_review():
    data = json.load(open('import-in-progress.json','r'))
    return {}

@blueprint.route('/spreadjs', auth=auth.public, methods=['GET', 'POST'])
@render_html()
def spreadjs():
    import xlrd
    from collections import defaultdict

    book = xlrd.open_workbook('app/samples/sample.xls')
    first_sheet = book.sheet_by_index(0)

    sheets = []
    for sheet in book.sheets():
        sd = defaultdict(dict)
        for rn in range(0, sheet.nrows):
            sd[rn] = []
            for cell in sheet.row(rn):
                sd[rn].append(cell.value)

        sheets.append(sd)

    return dict(
        sheets = sheets
    )

app.register_blueprint(blueprint)
