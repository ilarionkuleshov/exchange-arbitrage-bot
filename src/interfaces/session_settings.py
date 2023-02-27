from typing import Dict
from dataclasses import dataclass, field


@dataclass
class SessionSettings:
    session_id: int
    min_price_difference: float
    quote_currency: str
    min_quote_volume_24h: int
    exchanges: Dict[str, int] = field(default_factory=dict)
