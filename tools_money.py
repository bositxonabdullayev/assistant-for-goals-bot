from db import SessionLocal, Account, Category, Transaction
from decimal import Decimal
from datetime import datetime
from sqlalchemy import extract, func


def _default_account(db, user_id: int):
    acc = db.query(Account).filter_by(user_id=user_id, is_default=True).first()
    if not acc:
        acc = Account(user_id=user_id, name="Wallet", currency="UZS", is_default=True)
        db.add(acc)
        db.commit()
        db.refresh(acc)
    return acc


def add_tx(user_id: int, amount: str, ttype: str, category: str | None = None, note: str | None = None, date: str | None = None):
    db = SessionLocal()
    acc = _default_account(db, user_id)
    cat_id = None
    if category:
        cat = db.query(Category).filter_by(user_id=user_id, name=category).first()
        if not cat:
            cat = Category(user_id=user_id, name=category)
            db.add(cat)
            db.commit()
            db.refresh(cat)
        cat_id = cat.id
    dt = datetime.fromisoformat(date) if date else datetime.utcnow()
    tx = Transaction(
        user_id=user_id,
        account_id=acc.id,
        category_id=cat_id,
        amount=Decimal(amount),
        ttype=ttype,
        note=note,
        at=dt,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return {"ok": True, "tx_id": tx.id}


def report_current_month(user_id: int):
    db = SessionLocal()
    now = datetime.utcnow()
    rows = (
        db.query(Category.name, Transaction.ttype, func.sum(Transaction.amount))
        .outerjoin(Category, Category.id == Transaction.category_id)
        .filter(Transaction.user_id == user_id)
        .filter(extract("year", Transaction.at) == now.year)
        .filter(extract("month", Transaction.at) == now.month)
        .group_by(Category.name, Transaction.ttype)
        .all()
    )
    return [
        {"category": r[0] or "(no cat)", "type": r[1], "sum": str(r[2])}
        for r in rows
    ]
