from db import SessionLocal, Task, ColumnModel


def _ensure_column(db, user_id: int, name: str, order: int = 0):
    col = db.query(ColumnModel).filter_by(user_id=user_id, name=name).first()
    if not col:
        col = ColumnModel(user_id=user_id, name=name, order=order)
        db.add(col)
        db.commit()
        db.refresh(col)
    return col


def t_add(user_id: int, title: str, desc: str | None = None, due: str | None = None, column: str = "Today"):
    db = SessionLocal()
    col = _ensure_column(db, user_id, column, 0)
    t = Task(user_id=user_id, column_id=col.id, title=title, description=desc, due_at=due)
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"ok": True, "task_id": t.id}


def t_move(user_id: int, task_id: int, to_column: str):
    db = SessionLocal()
    col = _ensure_column(db, user_id, to_column, 0)
    t = db.query(Task).filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return {"ok": False, "error": "task_not_found"}
    t.column_id = col.id
    db.commit()
    return {"ok": True}


def t_done(user_id: int, task_id: int):
    return t_move(user_id, task_id, "Done")


def t_list(user_id: int):
    db = SessionLocal()
    cols = db.query(ColumnModel).filter_by(user_id=user_id).order_by(ColumnModel.order).all()
    out = []
    for c in cols:
        tasks = (
            db.query(Task)
            .filter_by(user_id=user_id, column_id=c.id)
            .order_by(Task.id.desc())
            .all()
        )
        out.append(
            {
                "column": c.name,
                "items": [
                    {"id": t.id, "title": t.title, "due": t.due_at}
                    for t in tasks
                ],
            }
        )
    if not out:
        for name in ["Today", "Doing", "Done"]:
            _ensure_column(db, user_id, name, 0)
    return out
