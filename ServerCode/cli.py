"""
Module representing the command-line interface (CLI)
"""
from typing import Optional
import click
from bubbleScan.repository.memrepo import MemRepo
from bubbleScan.use_cases.scantron_list import scantron_list_use_case

@click.command()
@click.option("--request", help="Specify a request for the CLI.")
def cli(request: Optional[str]):
    """
    Command-line interface function.

    :param request: str, an optional request parameter.
    """

    repo = MemRepo([])
    result = scantron_list_use_case(repo, request)
    click.echo(result)
    print(result)

if __name__ == "__main__":
    cli()
