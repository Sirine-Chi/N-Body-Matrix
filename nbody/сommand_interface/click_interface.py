import click

@click.group()
def cli():
    pass

@cli.command()
def generate_table():
    # Call to controller
    click.echo('Table succesfully generated!')

@cli.command()
def load_table():
    # Call to controller
    click.echo('Dropped the database')