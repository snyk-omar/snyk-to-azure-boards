import typer
from rich.console import Console

import snyk

from snyk_to_azure_boards import version


def get_client(token: str):
    client = snyk.SnykClient(token=token)
    return client


app = typer.Typer(
    name="snyk-to-azure-boards",
    help="CLI tool to convert Snyk issues to Azure Boards issues.",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(
            f"[yellow]snyk-to-azure-boards[/] version: [bold blue]{version}[/]"
        )
        raise typer.Exit()


@app.command()
def main(
    snyk_token: str = typer.Option(
        None,
        "--token",
        envvar="SNYK_TOKEN",
    ),
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the snyk-to-azure-boards package.",
    ),
) -> None:
    """
    Given a Snyk Project ID, get the issues and send them to Azure Boards.
    Must have a valid Snyk token either as a SNYK_TOKEN environment variable
    or submit it as an optional argument.
    """

    client = get_client(token=snyk_token)
    return None


if __name__ == "__main__":
    app()
