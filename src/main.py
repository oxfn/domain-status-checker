import asyncio
import logging

import click

from database import Database
from tasks import main
from utils import get_hosts

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
@click.option("-d", "--db", "db_file", default="domains.db", help="Database name")
@click.option("-n", "size", default=3, help="Domain length")
@click.option("-t", "--tld", "tld", default=".su", help="TLD")
@click.option("-r", "--recheck", "recheck", is_flag=True, help="Recheck")
def cli(db_file: str, size: int, tld: str, recheck: bool):
    task = main(Database(db_file), get_hosts(size, tld), recheck)
    asyncio.run(task)


if __name__ == "__main__":
    cli()
