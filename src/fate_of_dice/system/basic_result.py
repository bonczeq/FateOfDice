from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class BasicResult(ABC):
    user: Optional[str]
    descriptions: [str]
    priv_request: Optional[bool]
