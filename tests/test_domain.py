from archilog.domain import compute_transactions, Transaction
from archilog.data import MoneyPot, Expense
from datetime import datetime

def test_compute_transactions_equilibre_simple():
    # 1. PRÉPARATION (Arrange)
    expenses = [
        Expense(money_pot="Test", paid_by="Alice", amount=10.0, datetime=datetime.now()),
        Expense(money_pot="Test", paid_by="Bob", amount=20.0, datetime=datetime.now()),
        Expense(money_pot="Test", paid_by="Charlie", amount=30.0, datetime=datetime.now()),
    ]
    pot = MoneyPot(name="Test", expenses=expenses)
    
    # La moyenne est de 20€. 
    # Alice a payé 10 (doit 10). Bob a payé 20 (équilibré). Charlie a payé 30 (récupère 10).

    # 2. ACTION (Act)
    transactions = compute_transactions(pot)

    # 3. VÉRIFICATION (Assert)
    assert len(transactions) == 1, "Il ne devrait y avoir qu'une seule transaction"
    assert transactions[0].sender == "Alice", "Alice doit rembourser"
    assert transactions[0].receiver == "Charlie", "Charlie doit recevoir"
    assert transactions[0].amount == 10.0, "Le montant doit être de 10€"