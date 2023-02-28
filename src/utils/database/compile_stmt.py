from typing import Tuple

from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql.dml import ClauseElement


def compile_stmt(stmt: ClauseElement) -> Tuple[str, tuple]:
    stmt_compiled = stmt.compile(dialect=mysql.dialect())
    return (str(stmt_compiled), tuple(stmt_compiled.params.values()))
