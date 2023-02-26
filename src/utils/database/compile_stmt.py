from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql.dml import ClauseElement


def compile_stmt(stmt: ClauseElement) -> str:
    return str(
        stmt.compile(
            compile_kwargs={"literal_binds": True},
            dialect=mysql.dialect()
        )
    )
