import click
from trex.support.run import cli
from app import app
import app.model as m
from trex.support import quantum

@cli.command()
def load_data():
    app.drop_collections()
    app.create_collections()

    users = [
        dict(
            email = 'nigel@opcode.co.nz',
            password = 'password',
            display_name = 'Nigel McNie',
            country = 'NZ',
            timezone = 'Pacific/Auckland',
        ),
        dict(
            email = 'richard@opcode.co.nz',
            password = 'password',
            display_name = 'Richard Clark',
            country = 'NZ',
            timezone = 'Pacific/Auckland',
        ),
    ]

    for user_data in users:
        u = m.User(
            **user_data
        )
        u.set_password(user_data['password'])
        u.save()

