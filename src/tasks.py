# from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging
from typing import Iterable

from database import Database
from utils import get_domain_info


async def worker(name: str, db: Database, q: asyncio.Queue, recheck: bool = False):
    logger = logging.getLogger(name)

    while True:
        host = await q.get()

        logger.info("Host %s", host)

        async with db.lock:
            domain = db.get_domain(host)
        if not domain or (recheck and (not domain.tld or domain.is_expired)):
            domain = await get_domain_info(host)
            async with db.lock:
                domain = db.save_domain(domain)


async def main(db: Database, items: Iterable[str], recheck: bool = False, pool_size: int = 10):
    tasks = asyncio.Queue()
    for _ in items:
        await tasks.put(_)
    workers = [
        asyncio.create_task(worker(f"Worker {_+1}", db, tasks, recheck)) for _ in range(pool_size)
    ]
    await asyncio.gather(*workers)
