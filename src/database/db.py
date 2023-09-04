import logging
import sqlite3

from .models import Domain
from .queries import (
    SQL_INIT,
    SQL_SELECT_DOMAIN,
    SQL_SELECT_EMPTY_DOMAINS,
    SQL_UPSERT_DOMAIN,
)

logger = logging.getLogger(__name__)


class Database:
    """Database interface."""

    def __init__(self, path: str = None):
        """Initializer."""
        self.conn = self._open(path)
        self._init()

    def _open(self, path: str = None):
        """Opens DB connection."""
        return sqlite3.connect(path)

    def _init(self):
        """Initialize database."""
        self.conn.executescript(SQL_INIT)

    def get_domain(self, name: str) -> Domain:
        """Get domain record by domain name."""
        domain = None
        cur = self.conn.execute(SQL_SELECT_DOMAIN, (name,))
        row = cur.fetchone()
        cur.close()
        if row:
            logger.debug("Row %s", row)
            domain = Domain(*row)
        return domain

    def get_domains_for_update(self):
        cur = self.conn.execute(SQL_SELECT_EMPTY_DOMAINS)
        result = [Domain(*row) for row in cur.fetchall()]
        cur.close()
        return result

    def save_domain(self, domain: Domain) -> Domain:
        """Add or update domain record to database."""
        cur = self.conn.cursor()
        args = (
            domain.name,
            domain.ip,
            domain.tld,
            domain.status,
            domain.created,
            domain.expires,
        )
        cur.execute(SQL_UPSERT_DOMAIN, args)
        self.conn.commit()
        domain.id = cur.lastrowid
        return domain

    def close(self):
        self.conn.close()
