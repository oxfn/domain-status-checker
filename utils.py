import socket
from itertools import product
from typing import Generator, Union, Optional
from urllib.request import urlopen

CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"


def get_config():
    pass


def get_addr(host: str) -> Union[str, None]:
    try:
        return socket.gethostbyname(host)
    except:
        return None


def get_hosts(n: int, r: str) -> Generator:
    """Generates hosts by parameters."""
    for chars in product(CHARS, repeat=3):
        host = "".join(chars) + r
        yield host


def get_status(domain: str) -> bool:
    """Gets domain status from registrant."""
    url = "https://www.webnames.ru/domains/check?check_future=yes&domain_name=" + domain
    with urlopen(url) as resp:
        data = resp.read().decode("utf-8")
        if data.find("check-results__available") > -1:
            return True
        elif data.find("check-results__unavailable") > -1:
            return False
        else:
            raise Exception("Unrecognized response")

def get_host_info(domain: str) -> tuple[Optional[str], bool]:
    addr = get_addr(domain)
    status = False
    if addr is None:
        status = get_status(domain)
    else:
        status = True
    return addr, status
