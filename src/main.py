import logging
from time import sleep

import click

from database import Database
from utils import get_domain_info, get_hosts

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
@click.option("-d", "--db", "db_file", default="domains.db", help="Database name")
@click.option("-n", "size", default=3, help="Domain length")
@click.option("-t", "--tld", "tld", default=".su", help="TLD")
@click.option("-i", "--interval", "interval", default=0.5, help="Sleep interval")
@click.option("-r", "--recheck", "recheck", help="Recheck")
def cli(db_file: str, size: int, tld: str, interval: float, recheck: bool):
    db = Database(db_file)
    for host in get_hosts(size, tld):
        logger.info("Host %s", host)
        domain = db.get_domain(host)
        if not domain or (recheck and (not domain.tld or domain.is_expired)):
            domain = get_domain_info(host)
            domain = db.save_domain(domain)
            sleep(interval)
        logger.info(domain)


if __name__ == "__main__":
    cli()
