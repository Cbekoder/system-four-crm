from apps.factory.models import RawMaterialHistory, Sale
# from apps.fridge.models import Something
from apps.garden.models import SalaryPayment as GardenSalaryPayment
from apps.logistic.models import CarExpense, SalaryPayment as LogisticSalaryPayment, TransitExpense, TransitIncome
from apps.main.models import Income, Expense, MoneyCirculation
from apps.users.models import User


def get_remainder_data(start_date, end_date):
    incomes = list(Income.objects.all().values("created_at", "description", "amount", "currency_type"))
    expenses = list(Expense.objects.all().values("created_at", "description", "amount", "currency_type"))
    circulations = list(
        MoneyCirculation.objects.all().values("created_at", "description", "amount", "currency_type", "type"))

    money_income = [{"created_at": tx["created_at"], "description": tx["description"], "amount": tx["amount"],
                     "currency_type": tx["currency_type"]} for tx in circulations if tx["type"] == "get"]
    money_outcome = [{"created_at": tx["created_at"], "description": tx["description"], "amount": tx["amount"],
                      "currency_type": tx["currency_type"]} for tx in circulations if tx["type"] == "give"]

    sorted_income = sorted(incomes + money_income, key=lambda x: x["created_at"], reverse=True)
    sorted_outcome = sorted(expenses + money_outcome, key=lambda x: x["created_at"], reverse=True)
    return {"sorted_income": sorted_income, "sorted_outcome": sorted_outcome}

def calculate_remainder(date, user):
    incomes = [
        Sale.objects.filter(creator=user, created_at=date), 
        TransitIncome.objects.filter(creator=user, created_at=date), 
        Income.objects.filter(creator=user, created_at=date), 
        MoneyCirculation.objects.filter(creator=user, created_at=date, type='get')
    ]
    outcome = [
        RawMaterialHistory.objects.filter(creator=user, created_at=date),
        CarExpense.objects.filter(creator=user, created_at=date),
        GardenSalaryPayment.objects.filter(creator=user, created_at=date),
        LogisticSalaryPayment.objects.filter(creator=user, created_at=date),
        TransitExpense.objects.filter(creator=user, created_at=date),
        Expense.objects.filter(creator=user, created_at=date),
        MoneyCirculation.objects.filter(creator=user, created_at=date, type='give'),
    ]


def transaction_verify():
    pass