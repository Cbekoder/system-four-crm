from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Income, Expense, MoneyCirculation
from .serializers import MixedDataSerializer



def get_data(start_date, end_date):
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