"""
Description: This file contains the main entry point for the faag cli.
"""

import typer
from faag_cli.constants.app_types import AppTypes
from faag_cli.core.app_generator import AppGenerator
from faag_cli.utils.faag_utils import FaagUtils
from rich import print as rprint
from typer import Option, Typer

typer_app = Typer()  # Create a Typer instance


@typer_app.command(name="generate")
def app_gen(
    app_type: AppTypes = Option(
        AppTypes.FAST.value,
        "--app-type",
        "-at",
        help="Type of app to generate either flask or fast [default: fast]",
    ),
    app_name: str = Option(
        "sample_app",
        "--app-name",
        "-an",
        help="Name of the app to generate [default: sample_app]",
    ),
) -> None:
    FaagUtils.handle_app_folder_already_exists()  # Check if the app folder already exists
    app_type = app_type.value.lower()  # Get the app type
    if not app_type:
        rprint("[bold yellow]🧪️Warning: No app type was provided. Falling back to default type [fast][/bold yellow]")
        AppGenerator.gen("fast", app_name)

    # Check if the app type is valid
    if app_type and app_type not in ["flask", "fast"]:
        rprint(
            "[bold red]:police_car_light:Error: Invalid app type. Please provide valid app type (fast, flask)[/bold "
            "red]"
        )
        typer.Exit(code=1)

    if app_type and app_type in ["flask", "fast"]:
        # App generation starts here
        AppGenerator.gen(app_type, app_name)


@typer_app.command(name="feature")
def feature_gen() -> None:
    rprint("Feature generation is currently under development. Coming soon")


if __name__ == "__main__":
    typer_app()
