import json

from typing import Dict, List, Any
from dataclasses import dataclass, field, asdict

from sqlalchemy import create_engine, select

from database.models import Session
from utils import safe_execute
from utils.database import mysql_connection_url


@dataclass
class SessionSettings:
    session_id: int
    min_price_difference: float
    quote_currency: str
    min_quote_volume_24h: int
    exchanges: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_db(cls, raw_session_id: str):
        session_id = safe_execute(int, raw_session_id)
        if session_id is None:
            raise Exception("Invalid session_id was passed")
        with create_engine(mysql_connection_url()).connect() as connection:
            raw_session_settings = connection.execute(
                select(Session.settings).where(Session.id == session_id)
            )
            raw_session_settings = list(raw_session_settings)
            if len(raw_session_settings) != 1 or len(raw_session_settings[0]) != 1:
                raise Exception(
                    f"Session with id = {session_id} does not exist in the database"
                )
            session_settings = safe_execute(json.loads, raw_session_settings[0][0])
            if session_settings is None:
                raise Exception(
                    f"Invalid settings specified for the session (id = {session_id})"
                )
            return cls(session_id, **session_settings)

    def to_dict(self, exclude_keys: List[str] = []) -> Dict[str, Any]:
        data_dict = asdict(self)
        return {key:value for key, value in data_dict.items() if key not in exclude_keys}
