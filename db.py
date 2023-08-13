import sqlite3
from datetime import datetime

SQL_INIT = """
CREATE TABLE IF NOT EXISTS domains (
    domain TEXT PRIMARY KEY,
    ip TEXT,
    registered INTEGER DEFAULT 0
);
"""

SQL_SELECT = """SELECT * FROM domains WHERE domain=?;"""

SQL_UPSERT = """
INSERT INTO domains (domain, ip, registered)
VALUES (?1, ?2, ?3)
ON CONFLICT(domain) DO UPDATE
SET ip=?2, registered=?3
WHERE domain=?1;
"""

class Database:
    def __init__(self, path: str = None):
        """Initializer."""
        self.conn = self._open(path)
        self._init()

    def _open(self, path: str = None):
        """Opens DB connection."""
        if path is None:
            path = datetime.now().strftime("%Y%m%d%H%M%s.db")
        return sqlite3.connect(path)
    
    def _init(self):
        self.conn.execute(SQL_INIT)

    def get(self, domain):
        cur = self.conn.execute(SQL_SELECT, (domain,))
        row = cur.fetchone()
        cur.close()
        return row

    def set(self, domain: str, ip: str, registered: bool) -> None:
        """Adds record to database."""
        self.conn.execute(SQL_UPSERT, (domain, ip, 1 if registered else 0))
        self.conn.commit()

    def close(self):
        self.conn.close()
