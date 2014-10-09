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
            email        = 'nigel@opcode.co.nz',
            password     = 'password',
            display_name = 'Nigel McNie',
            country      = 'NZ',
            timezone     = 'Pacific/Auckland',
            role         = 'developer',
        ),
        dict(
            email        = 'richard@opcode.co.nz',
            password     = 'password',
            display_name = 'Richard Clark',
            country      = 'NZ',
            timezone     = 'Pacific/Auckland',
            role         = 'developer',
        ),
        dict(
            email        = 'martyn@opcode.co.nz',
            password     = 'password',
            display_name = 'Martyn Smith',
            country      = 'NZ',
            timezone     = 'Pacific/Auckland',
            role         = 'developer',
        ),
        dict(
            email        = 'lilliangrace@wikinewzealand.org',
            password     = 'password',
            display_name = 'Lillian Grace',
            country      = 'NZ',
            timezone     = 'Pacific/Auckland',
        ),
        dict(
            email        = 'amyhooper@wikinewzealand.org',
            password     = 'password',
            display_name = 'Amy Hooper',
            country      = 'NZ',
            timezone     = 'Pacific/Auckland',
        ),
        dict(
            email        = 'rob@prng.net',
            password     = 'password',
            display_name = 'Rob Isaac',
            country      = 'NZ',
            timezone     = 'Pacific/Auckland',
        ),
    ]

    for user_data in users:
        u = m.User(
            **user_data
        )
        u.set_password(user_data['password'])
        u.save()

