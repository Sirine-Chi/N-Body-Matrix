import click
from nbody.modules import controller as ctrl

@click.command()
@click.version_option(ctrl.version['VERSION'], prog_name=ctrl.version['NAME'])
def hello():
    pass

@click.command
def exit():
    pass

@click.command()
@click.option('--on')
@click.option('--off')
def hints(is_on: bool = True):
    if is_on:
        pass
    else:
        pass

    
