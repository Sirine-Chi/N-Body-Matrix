import click

from nbody.gui.gui_runner import run_gui
from nbody.start import start


@click.command()
@click.option(
    "--gui",
    default=False,
    is_flag=True,
    help="Set this if you want to use GUI.",
)
def main(gui: bool):
    if gui:
        run_gui()
    else:
        start()


main()
