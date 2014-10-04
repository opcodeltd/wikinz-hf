import click
from trex.support.run import cli
from app import app
import app.model as m
from trex.support import quantum

@cli.command()
def load_dummy_data():
    app.drop_collections()
    app.create_collections()

    data = [
        dict(
            name = 'Year',
            type = 'date',
            series = ['2001', '2002', '2003', '2004'],
        ),
        dict(
            name = 'Frogs',
            type = 'number',
            series = [1, 8, 2, 5],
        ),
        dict(
            name = 'Ponies',
            type = 'string',
            series = ['thing', 'wobble', 'pony'],
        ),
    ]


    chartable = m.Chartable(
        name = 'Test Chartable'
    ).save()

    for column_data in data:
        type = column_data['type']
        if type == 'date':
            Model = m.ChartableColumnDate
            model_data = [quantum.parse_date('%s-01-01' % x) for x in column_data['series']]
        elif type == 'number':
            Model = m.ChartableColumnNumber
            model_data = column_data['series']
        elif type == 'string':
            Model = m.ChartableColumnString
            model_data = column_data['series']
        else:
            raise Exception("Don't know that type")

        Model(
            chartable = chartable,
            name = column_data['name'],
            data = model_data,
        ).save()
