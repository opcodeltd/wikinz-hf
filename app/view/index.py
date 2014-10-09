# coding=utf-8

from __future__ import absolute_import
from app import app
from app.support import auth
from trex.flask import AuthBlueprint, render_html, flash
from trex.support import wtf, quantum
from flask import abort, g, redirect, url_for, make_response, request
import json
import app.model as m


blueprint = AuthBlueprint('index', __name__)


@blueprint.route('/', auth=auth.public)
@render_html()
def index():
    if not g.user:
        return dict(_template='index_anonymous')

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
        title = wtf.StringField('Title')
        source = wtf.StringField('Source', description='e.g. Statistics New Zealand')
        data_file = wtf.FileField(
            'File to import',
            [wtf.validators.Required()],
            allow_clear = False,
        )

    form = Form()

    if form.validate_on_submit():
        m.Source(title=form.title.data,
                 source=form.source.data,
                 file=form.data_file.data,
                 created=quantum.now('Pacific/Auckland'),
                 creator=g.user,
                 filename=form.data_file.data.file.filename).save()
        flash('Source "%s" added' % form.title.data)
        return redirect(url_for('index.sources'))

    return dict(form=form)

@blueprint.route('/sources', auth=auth.public)
@render_html()
def sources():
    return dict(sources=m.Source.objects().order_by('title'))

@blueprint.route('/sources/<source_id>/download', auth=auth.public)
def download_source(source_id):
    source = m.Source.objects.get(id=source_id)
    response = make_response(source.file.file.read())
    response.headers["Content-Disposition"] = "attachment; filename=%s" % source.filename
    return response

@blueprint.route('/tables', auth=auth.public)
@render_html()
def tables():
    return dict(tables=m.Table.objects().order_by('title'))

@blueprint.route('/tables/<table_id>/view', auth=auth.public)
@render_html()
def view_table(table_id):
    table = m.Table.objects.get(id=table_id)
    return {'table': table}

@blueprint.route('/tables/<table_id>/download', auth=auth.public)
def download_table(table_id):
    table = m.Table.objects.get(id=table_id)
    # SOMETHING GOES HERE TO MAKE THINGS GO
    csv_output = "OH GOD, NOT IMPLEMENTED, RUN ZOMBIES"
    response = make_response(csv_output)
    response.headers["Content-Disposition"] = "attachment; filename=table.csv"
    return response

@blueprint.route('/graphs/<graph_id>/view', auth=auth.public)
@render_html()
def view_graph(graph_id):
    graph = m.Graph.objects.get(id=graph_id)
    return {'graph': graph}

@blueprint.route('/tables/<table_id>/create_graph', auth=auth.public, methods=['GET','POST'])
@render_html()
def create_graph(table_id):
    table = m.Table.objects.get(id=table_id)
    axes = [('-1', 'Use column titles for X axis')]
    choices = []
    for i, col in enumerate(table.data['cols']):
        axes.append((str(i), col['title']['value']))
        choices.append((str(i), col['title']['value']))

    class Form(wtf.Form):
        title = wtf.StringField('Title')
        description = wtf.StringField('Source')
        xaxis = wtf.SelectField('X Axis Column', choices=axes)
        columns = wtf.CheckListField('Series', choices=choices)

    form = Form()

    if form.validate_on_submit():
        graph = m.Graph(title=form.title.data,
                 table=table,
                 created=quantum.now('Pacific/Auckland'),
                 creator=g.user,
                 axis=int(form.xaxis.data),
                 cols=[int(x) for x in form.columns.data])
        graph.save()
        flash("Graph created")
        return redirect(url_for('index.view_graph', graph_id=graph.id))

    return dict(form=form)

@blueprint.route('/graphs/<graph_id>/edit', auth=auth.public, methods=['GET','POST'])
@render_html()
def edit_graph(graph_id):
    graph = m.Graph.objects.get(id=graph_id)
    axes = [(None, 'Use column titles for X axis')]
    choices = []
    for i, col in enumerate(graph.table.data['cols']):
        axes.append((str(i), col['title']['value']))
        choices.append((str(i), col['title']['value']))

    class Form(wtf.Form):
        title = wtf.StringField('Title')
        description = wtf.StringField('Source')
        xaxis = wtf.SelectField('X Axis Column', choices=axes)
        columns = wtf.CheckListField('Series', choices=choices)

    form = Form(obj=graph)

    if form.validate_on_submit():
        graph.title = form.title.data
        graph.axis = form.xaxis.data
        graph.cols = form.columns.data
        graph.save()
        flash("Graph updated")
        return redirect(url_for('index.view_graph', graph_id=graph.id))

    return dict(form=form)

@blueprint.route('/source/<source_id>/delete', auth=auth.public, methods=['POST'])
def delete_source(source_id):
    source = m.Source.objects.get(id=source_id)
    if m.Table.objects(source=source).count() > 0:
        flash('Source has existing tables, delete tables first')
        return redirect(url_for('index.sources'), 302)
    source.delete()
    flash('Source deleted')
    return redirect(url_for('index.sources'), 302)

@blueprint.route('/tables/<table_id>/delete', auth=auth.public, methods=['POST'])
def delete_table(table_id):
    table = m.Table.objects.get(id=table_id)
    if m.Graph.objects(table=table).count() > 0:
        flash('Table has existing graphs, delete graphs first')
        return redirect(url_for('index.tables'), 302)
    table.delete()
    flash('Table deleted')
    return redirect(url_for('index.tables'), 302)

@blueprint.route('/graphs', auth=auth.public)
@render_html()
def graphs():
    return dict(graphs=m.Graph.objects().order_by('title'))

@blueprint.route('/graph/<graph_id>/delete', auth=auth.public, methods=['POST'])
def delete_graph(graph_id):
    graph = m.Graph.objects.get(id=graph_id)
    graph.delete()
    flash('Graph deleted')
    return redirect(url_for('index.graphs'), 302)

@blueprint.route('/table/<table_id>/charter', auth=auth.public, methods=['GET', 'POST'])
@render_html()
def charter():
    return {}

@blueprint.route('/import-review', auth=auth.public, methods=['GET', 'POST'])
@render_html()
def import_review():
    data = json.load(open('import-in-progress.json','r'))
    return {}

@blueprint.route('/spreadjs/<source_id>', auth=auth.public)
@render_html()
def spreadjs(source_id):
    source = m.Source.get_404(id=source_id)

    import xlrd
    from collections import defaultdict

    book = xlrd.open_workbook(file_contents=source.file.file.get().read())
    first_sheet = book.sheet_by_index(0)

    sheets = []
    for sheet in book.sheets():
        sd = defaultdict(dict)
        for rn in range(0, sheet.nrows):
            sd[rn] = []
            for cell in sheet.row(rn):
                sd[rn].append(cell.value)

        sheets.append(sd)

    column_view_tpl = """
    <tr id="column-<%= model.cid %>">
        <th data-select-target="input-title-<%= model.cid %>" class="th-title">Title:</th>
        <td data-select-target="input-title-<%= model.cid %>" class="td-title"><input type="text" value="<%= model.get('title') %>"data-select-target="input-title-<%= model.cid %>" id="input-title-<%= model.cid %>" class="form-control"></td>
        <th data-select-target="input-series-<%= model.cid %>" class="th-series">Values:</th>
        <td data-select-target="input-series-<%= model.cid %>" class="td-series"><input type="text" value="<%= model.get('series') %>" data-select-target="input-series-<%= model.cid %>" id="input-series-<%= model.cid %>" class="form-control"></td>
        <td class="controls"><button type="button" class="btn btn-danger remove">&times;</button><input type="hidden" class="input-dump-<%= model.cid %>" name="column-<%= model.cid %>"></td>
    </tr>
    """

    return dict(
        source_id = source.id,
        sheets = sheets,
        column_view_tpl = column_view_tpl,
    )

@blueprint.route('/spreadjs/<source_id>/save', auth=auth.public, methods=['POST'])
def spreadjs_save(source_id):
    source = m.Source.get_404(id=source_id)

    column_data = json.loads(request.form.get('columns'))

    data = dict(cols=[])

    for column in column_data:
        data['cols'].append(dict(
            title = dict(value=column['title']),
            values = [dict(value=x) for x in column['values']],
        ))

    table = m.Table(
        title = request.form.get('table-title'),
        description = request.form.get('table-description'),
        creator = g.user,
        source = source,
        data = data,
    )
    table.save()

    flash('Table created')
    return redirect(url_for('index.view_table', table_id=table.id))

app.register_blueprint(blueprint)
