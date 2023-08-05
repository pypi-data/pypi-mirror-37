import click
import .db as db

@click.command()
def hello():
    click.echo("coucou")
