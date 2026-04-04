from dataclasses import dataclass
from archilog.data import MoneyPot, get_money_pot

@dataclass
class MeanDeviation:
    name: str
    amount: float

@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float

def get_money_pot_details(money_pot_name: str) -> tuple[MoneyPot, list[Transaction]]:
    money_pot = get_money_pot(money_pot_name)
    return money_pot, compute_transactions(money_pot)

def compute_transactions(money_pot: MoneyPot) -> list[Transaction]:
    if not money_pot.expenses:
        return []

    mean = sum(e.amount for e in money_pot.expenses) / len(money_pot.expenses)
    
    debtors = []
    creditors = []
    
    for e in money_pot.expenses:
        diff = e.amount - mean
        if diff < -0.01:
            debtors.append([e.paid_by, abs(diff)])
        elif diff > 0.01:
            creditors.append([e.paid_by, diff])
            
    transactions: list[Transaction] = []
    i, j = 0, 0
    
    while i < len(debtors) and j < len(creditors):
        debtor_name, debt = debtors[i]
        creditor_name, credit = creditors[j]
        
        amount_to_pay = min(debt, credit)
        transactions.append(Transaction(sender=debtor_name, receiver=creditor_name, amount=round(amount_to_pay, 2)))
        
        debtors[i][1] -= amount_to_pay
        creditors[j][1] -= amount_to_pay
        
        if debtors[i][1] < 0.01: i += 1
        if creditors[j][1] < 0.01: j += 1
            
    return transactions