from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Domain:
    id: Optional[int]
    name: str
    ip: Optional[str]
    tld: Optional[str]
    registrar: Optional[str]
    status: Optional[str]
    created: Optional[str]
    expires: Optional[str]

    @property
    def is_expired(self):
        """Check if domain has expired."""
        return self.expires and self.expires <= datetime.utcnow().isoformat()


@dataclass
class Nameserver:
    id: Optional[int]
    value: str


@dataclass
class Email:
    id: Optional[int]
    value: str


__all__ = [
    "Domain",
]
