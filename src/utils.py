import asyncio
import logging
import socket
from itertools import product
from typing import Iterator, Optional

import whois

from database import Domain

logger = logging.getLogger(__name__)

CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"


def get_addr(host: str) -> Optional[str]:
    try:
        return socket.gethostbyname(host)
    except Exception:
        return None


def get_hosts(n: int, r: str) -> Iterator[str]:
    """Generates hosts by parameters."""
    for chars in product(CHARS, repeat=3):
        host = "".join(chars) + r
        yield host


def get_whois(host: str) -> bool:
    """Get whois info for host."""
    try:
        result = whois.get(host)
    except Exception as e:
        logger.exception("WHOIS ERROR: %s", e)
        result = {}
    logger.debug("WHOIS: %s", result)
    return result


def get_iso_date_field(data: dict, field: str) -> str:
    val = data.get(field)
    return val.isoformat() if val else None


def get_whois_statuses(data: dict) -> list[str]:
    result = []
    for s in data.get("status", "").split(","):
        s = s.strip()
        if s:
            result.append(s)
    return result


async def get_domain_info(domain: str) -> Domain:
    """Get full domain info."""
    addr = await asyncio.get_running_loop().run_in_executor(None, lambda: get_addr(domain))
    whois = await asyncio.get_running_loop().run_in_executor(None, lambda: get_whois(domain))
    return Domain(
        id=None,
        name=domain,
        ip=addr,
        tld=whois.get("tld"),
        registrar=whois.get("registrar"),
        status=whois.get("status"),
        created=get_iso_date_field(whois, "creation_date"),
        expires=get_iso_date_field(whois, "expiration_date"),
    )
