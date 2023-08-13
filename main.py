#!/usr/bin/env python

import click
import csv
from time import sleep
from utils import get_hosts, get_host_info
from db import Database


@click.command()
@click.option("-d", default="domains.db", help="Database name")
@click.option("-n", default=3, help="Domain length")
@click.option("-r", default=".su", help="TLD")
def cli(d: str, n: int, r: str):
    """CLI entry point.

    Options:
      -n - length of 2nd level name
      -r - root domain (1st level)
    """

    db = Database(d)

    for host in get_hosts(n, r):
        error, message = False, None
        row = db.get(host)
        if row:
            addr, status = row[1], bool(row[2])
        else:
            try:
                addr, status = get_host_info(host)
            except Exception as e:
                message = f"error: {e}"
                error = True
        if not message:
            message = 'registered' if status else "AVAILABLE"
        click.echo(f"{host},{addr},{message}")
        if not error:
            db.set(host, addr, status)
        if not row:
            sleep(1)



if __name__ == "__main__":
    cli()
