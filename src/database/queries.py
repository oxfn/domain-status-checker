SQL_INIT = """
    CREATE TABLE IF NOT EXISTS domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ip TEXT,
        tld TEXT,
        registrar TEXT,
        status TEXT,
        created TEXT,
        expires TEXT
    );
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    CREATE TABLE IF NOT EXISTS domain_status (
        domain_id INTEGER NOT NULL,
        status_id INTEGER NOT NULL,
        PRIMARY KEY (domain_id, status_id)
    );
    CREATE UNIQUE INDEX IF NOT EXISTS idx_domain_name ON domains (name);
"""


SQL_SELECT_DOMAIN = """
    SELECT id, name, ip, tld, registrar, status, created, expires
    FROM domains
    WHERE name=?;
"""

SQL_SELECT_EMPTY_DOMAINS = """
    SELECT id, name, ip, tld, status, created, expires
    FROM domains
    WHERE tld IS NULL
"""


SQL_SELECT_STATUSES = """
    SELECT s.name FROM status AS s
    INNER JOIN domain_status AS ds ON ds.status_id=s.id
    WHERE ds.domain_id=?
"""


SQL_UPSERT_DOMAIN = """
    INSERT INTO domains (name, ip, tld, status, created, expires)
        VALUES (?1, ?2, ?3, ?4, ?5, ?6)
    ON CONFLICT(name) DO UPDATE
        SET ip=?2, tld=?3, status=?4, created=?5, expires=?6
        WHERE name=?1
"""

SQL_SELECT_STATUSES = """SELECT id, name FROM status"""

SQL_SELECT_STATUS = """SELECT id, name FROM status WHERE name=?"""

SQL_INSERT_STATUS = """INSERT INTO status (name) VALUES (?) RETURNING id"""

SQL_SELECT_DOMAIN_STATUS = """"""

SQL_DELETE_DOMAIN_STATUS = """
    DELETE FROM domain_status
    WHERE domain_id=? AND status_id=?
"""
