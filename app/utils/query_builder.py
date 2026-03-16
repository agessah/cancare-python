from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import Select


def apply_filters(
    stmt: Select,
    model,
    filters: dict,
):
    for field, value in filters.items():

        if not hasattr(model, field):
            continue  # Ignore invalid fields safely

        column: InstrumentedAttribute = getattr(model, field)

        if value is None:
            continue

        stmt = stmt.where(column == value)

    return stmt


def apply_search(stmt: Select, model, search: str, fields: list[str]):
    if not search:
        return stmt

    from sqlalchemy import or_

    conditions = [
        getattr(model, field).ilike(f"%{search}%")
        for field in fields
        if hasattr(model, field)
    ]

    return stmt.where(or_(*conditions))


def apply_sort(stmt: Select, model, sort: str):
    if not sort:
        return stmt

    desc = sort.startswith("-")
    field = sort[1:] if desc else sort

    if not hasattr(model, field):
        return stmt  # Safe fallback

    column = getattr(model, field)

    if desc:
        return stmt.order_by(column.desc())
    return stmt.order_by(column.asc())