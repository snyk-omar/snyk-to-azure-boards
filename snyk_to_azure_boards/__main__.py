import logging

import snyk
import typer
from rich.console import Console
from snyk.models import Organization

from snyk_to_azure_boards import version

# Logging Configuration
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(name)-30s %(levelname)-8s %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# Snyk Methods
def get_client(token: str) -> snyk.SnykClient:
    """
    Get Snyk client to work with the Snyk API
    Args:
        token (str): Snyk API token
    Returns:
        snyk.SnykClient: The client object
    """
    client = snyk.SnykClient(token=token)
    return client


def get_org_by_id(client: snyk.SnykClient, org_id: str) -> Organization:
    org = client.organizations.get(org_id)
    return org


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
    org_id: str = typer.Argument(
        None, help="Organization ID of the org you want to pull project IDs from."
    ),
    snyk_token: str = typer.Option(
        None,
        "--token",
        "-t",
        envvar="SNYK_TOKEN",
    ),
    debug: bool = typer.Option(False, "--debug", "-d"),
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
    # Set the default logging level
    logger.setLevel(logging.INFO)

    if debug:
        # Show all debug messages
        logger.setLevel(logging.DEBUG)
        logger.debug("Hey, you did it! We're in debug mode!")

    if org_id is None:
        logger.warning("Organization ID is missing.")
        raise typer.BadParameter(message="Missing the Organization ID parameter.")

    client = get_client(token=snyk_token)

    org = get_org_by_id(client, org_id=org_id)
    logger.info(org.name)
    return None


if __name__ == "__main__":
    app()
