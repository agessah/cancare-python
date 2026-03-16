from sqlalchemy import event
from sqlalchemy.orm import Session
from contextvars import ContextVar
from datetime import datetime


# Context variable to store current user ID per request
current_user_id: ContextVar[int | None] = ContextVar(
    "current_user_id",
    default=None
)

@event.listens_for(Session, "before_flush")
def update_audit_fields(session, flush_context, instances):
    user_id = current_user_id.get()

    if user_id is None:
        return

    for obj in session.new:
        if hasattr(obj, "created_by"):
            obj.created_by = user_id
            obj.updated_by = user_id

    for obj in session.dirty:
        if hasattr(obj, "updated_by"):
            obj.updated_by = user_id
