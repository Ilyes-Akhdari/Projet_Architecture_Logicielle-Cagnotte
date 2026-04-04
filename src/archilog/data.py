import os
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table, Column, String, Float, DateTime, MetaData, create_engine, select, insert, delete
from sqlalchemy.exc import IntegrityError
from archilog.config import config

# --- 1. CONFIGURATION SQLALCHEMY ---
engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
metadata_obj = MetaData()

expenses_table = Table(
    "expenses",
    metadata_obj,
    Column("money_pot", String, primary_key=True),
    Column("paid_by", String, primary_key=True),
    Column("amount", Float, nullable=False),
    Column("datetime", DateTime, nullable=False, default=datetime.now)
)

def init_database():
    metadata_obj.create_all(engine)

# --- 2. STRUCTURES DE DONNÉES (Dataclasses) ---
@dataclass
class Expense:
    paid_by: str
    amount: float
    datetime: datetime

@dataclass
class MoneyPot:
    name: str
    expenses: list[Expense]

# --- 3. REQUÊTES BASE DE DONNÉES ---
def create_expense(money_pot: str, paid_by: str, amount: float):
    with engine.begin() as conn:
        stmt = insert(expenses_table).values(
            money_pot=money_pot,
            paid_by=paid_by,
            amount=amount,
            datetime=datetime.now()
        )
        conn.execute(stmt)

def delete_expense(money_pot: str, paid_by: str):
    with engine.begin() as conn:
        stmt = delete(expenses_table).where(
            (expenses_table.c.money_pot == money_pot) & 
            (expenses_table.c.paid_by == paid_by)
        )
        conn.execute(stmt)

def delete_money_pot(money_pot: str):
    with engine.begin() as conn:
        stmt = delete(expenses_table).where(expenses_table.c.money_pot == money_pot)
        conn.execute(stmt)

def get_all_money_pots():
    with engine.connect() as conn:
        stmt = select(expenses_table.c.money_pot).distinct()
        rows = conn.execute(stmt).fetchall()
        return [MoneyPot(name=row[0], expenses=[]) for row in rows]

def get_money_pot(name: str) -> MoneyPot:
    """Récupère une cagnotte spécifique et toutes ses dépenses."""
    with engine.connect() as conn:
        stmt = select(expenses_table).where(expenses_table.c.money_pot == name)
        rows = conn.execute(stmt).fetchall()
        
        # On recrée les objets Expense avec le vrai type datetime qui vient de la BDD
        expenses = [
            Expense(paid_by=row.paid_by, amount=row.amount, datetime=row.datetime)
            for row in rows
        ]
        return MoneyPot(name=name, expenses=expenses)