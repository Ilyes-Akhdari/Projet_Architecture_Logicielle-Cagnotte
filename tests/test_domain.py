from archilog.domain import compute_transactions, Transaction
from archilog.data import MoneyPot, Expense
from datetime import datetime


def make_pot(name, *expenses):
    """Helper : crée un MoneyPot à partir de tuples (paid_by, amount)."""
    return MoneyPot(
        name=name,
        expenses=[
            Expense(money_pot=name, paid_by=p, amount=a, datetime=datetime.now())
            for p, a in expenses
        ]
    )


# --- CAS 1 : équilibre simple (3 personnes) ---
def test_compute_transactions_equilibre_simple():
    # Moyenne = 20€. Alice doit 10 à Charlie.
    pot = make_pot("Test", ("Alice", 10.0), ("Bob", 20.0), ("Charlie", 30.0))
    transactions = compute_transactions(pot)

    assert len(transactions) == 1
    assert transactions[0].sender == "Alice"
    assert transactions[0].receiver == "Charlie"
    assert transactions[0].amount == 10.0


# --- CAS 2 : cagnotte vide → aucune transaction ---
def test_compute_transactions_cagnotte_vide():
    pot = MoneyPot(name="Vide", expenses=[])
    transactions = compute_transactions(pot)

    assert transactions == []


# --- CAS 3 : tout le monde a payé pareil → quitte ---
def test_compute_transactions_tout_quitte():
    pot = make_pot("Quitte", ("Alice", 15.0), ("Bob", 15.0), ("Charlie", 15.0))
    transactions = compute_transactions(pot)

    assert transactions == []


# --- CAS 4 : deux personnes, l'une doit à l'autre ---
def test_compute_transactions_deux_personnes():
    # Moyenne = 25€. Alice a payé 10 (doit 15). Bob a payé 40 (récupère 15).
    pot = make_pot("Duo", ("Alice", 10.0), ("Bob", 40.0))
    transactions = compute_transactions(pot)

    assert len(transactions) == 1
    assert transactions[0].sender == "Alice"
    assert transactions[0].receiver == "Bob"
    assert transactions[0].amount == 15.0
