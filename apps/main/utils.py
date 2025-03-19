from datetime import datetime, time
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from apps.common.utils import convert_currency
from apps.factory.models import RawMaterialHistory, Sale, SalaryPayment as WorkerSalaryPayment
# from apps.fridge.models import Something
from apps.garden.models import SalaryPayment as GardenSalaryPayment
from apps.logistic.models import CarExpense, SalaryPayment as LogisticSalaryPayment, TransitExpense, TransitIncome
from apps.main.models import Income, Expense, MoneyCirculation, DailyRemainder
from apps.users.models import User


def get_remainder_data(start_date, end_date):
    incomes = list(Income.objects.all().values("created_at", "description", "amount", "currency_type"))
    expenses = list(Expense.objects.all().values("created_at", "description", "amount", "currency_type"))
    circulations = list(
        MoneyCirculation.objects.all().values("created_at", "description", "amount", "currency_type", "type"))

    money_income = [
        {
            "created_at": tx["created_at"],
            "description": tx["description"],
            "amount": tx["amount"],
            "currency_type": tx["currency_type"]
        }
        for tx in circulations if tx["type"] == "get"
    ]
    money_outcome = [{"created_at": tx["created_at"], "description": tx["description"], "amount": tx["amount"],
                      "currency_type": tx["currency_type"]} for tx in circulations if tx["type"] == "give"]

    sorted_income = sorted(incomes + money_income, key=lambda x: x["created_at"], reverse=True)
    sorted_outcome = sorted(expenses + money_outcome, key=lambda x: x["created_at"], reverse=True)
    return {"sorted_income": sorted_income, "sorted_outcome": sorted_outcome}


def calculate_remainder(date, user):
    start_of_day = timezone.make_aware(datetime.combine(date, time.min))
    end_of_day = timezone.make_aware(datetime.combine(date, time.max))

    remainder = 0
    incomes = [
        Sale.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day)),
        TransitIncome.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day)),
        Income.objects.filter(user=user, created_at__range=(start_of_day, end_of_day)),
        MoneyCirculation.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day), type='get')
    ]
    outcomes = [
        RawMaterialHistory.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day)),
        CarExpense.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day)),
        GardenSalaryPayment.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day)),
        LogisticSalaryPayment.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day)),
        TransitExpense.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day)),
        Expense.objects.filter(user=user, created_at__range=(start_of_day, end_of_day)),
        MoneyCirculation.objects.filter(creator=user, created_at__range=(start_of_day, end_of_day), type='give'),
    ]

    for outcome in outcomes:
        for obj in outcome:
            if obj.currency_type == "UZS":
                remainder -= obj.amount
            else:
                remainder -= convert_currency("UZS", obj.currency_type, obj.amount)

    for income in incomes:
        for obj in income:
            if obj.currency_type == "UZS":
                remainder += obj.amount
            else:
                remainder += convert_currency("UZS", obj.currency_type, obj.amount)

    return remainder


def verification_transaction():
    transactions = []

    ###### Factory #######
    raw_material_objects = RawMaterialHistory.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in raw_material_objects:
        unique_id = f"FA-RM-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator": str(obj.creator.get_full_name()),
            "section": "Korzinka seh",
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'curren cy_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })

    worker_salary = WorkerSalaryPayment.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in worker_salary:
        unique_id = f"FA-SP-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator": str(obj.creator.get_full_name()),
            "section": "Korzinka seh",
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })


    sales = Sale.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in sales:
        unique_id = f"FA-SL-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })

    ####### Fridge #############


    ######## Garden ###########

    gardener_salary = GardenSalaryPayment.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in gardener_salary:
        unique_id = f"GA-SP-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator": str(obj.creator.get_full_name()),
            "section": "Bog'",
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })


    ###### Logistic ###########

    car_expenses = CarExpense.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in car_expenses:
        unique_id = f"LO-CE-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator": str(obj.creator.get_full_name()),
            "section": "Logistika",
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })


    driver_salary = LogisticSalaryPayment.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in driver_salary:
        unique_id = f"LO-SP-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator": str(obj.creator.get_full_name()),
            "section": "Logistika",
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })



    transit_expenses = TransitExpense.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in transit_expenses:
        unique_id = f"LO-TE-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator": str(obj.creator.get_full_name()),
            "section": "Logistika",
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })


    transit_incomes = TransitIncome.objects.filter(creator__role="admin", status="new").select_related('creator')
    for obj in transit_incomes:
        unique_id = f"LO-TI-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator": str(obj.creator.get_full_name()),
            "section": "Logistika",
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })

    ######## Main ############

    expenses = Expense.objects.filter(user__role="admin", status="new").select_related('user')
    for obj in expenses:
        unique_id = f"MA-EX-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator":str(obj.user.get_full_name()),
            "section": obj.section,
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })

    incomes = Income.objects.filter(user__role="admin", status="new").select_related('user')
    for obj in incomes:
        unique_id = f"MA-IN-{obj.id}"
        transactions.append({
            "unique_id": unique_id,
            "creator":str(obj.user.get_full_name()),
            "section": obj.section,
            "description": getattr(obj, 'description', 'No description'),
            "amount": float(getattr(obj, 'amount', 0.0)),
            "currency_type": getattr(obj, 'currency_type', 'UZS'),
            "updated_at": obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at,
            "created_at": obj.created_at,
        })

    return transactions


def verify_transaction(unique_id, action):
    try:
        app_label, model_label, obj_id = unique_id.split("-")
    except ValueError:
        raise ValueError("Noto'g'ri unique_id formati. Format: APP-MODEL-ID")

    if action not in ["verify", "cancel"]:
        raise ValueError("Action faqat 'verify' yoki 'cancel' bo'lishi mumkin")

    app_model_map = {
        "FA": {"RM": RawMaterialHistory, "SP": WorkerSalaryPayment, "SL": Sale},
        # "FR": {"ST": "Storage"},
        "GA": {"SP": GardenSalaryPayment},
        "LO": {"CE": CarExpense, "SP": LogisticSalaryPayment, "TE": TransitExpense, "TI": TransitIncome},
        "MA": {"EX": Expense, "IN": Income},
    }

    if app_label not in app_model_map.keys():
        raise ValueError(f"Noto'g'ri unique_id: {unique_id}")

    if model_label not in app_model_map[app_label].keys():
        raise ValueError(f"Noto'g'ri unique_id: {unique_id}")

    model = app_model_map[app_label][model_label]
    try:
        obj = model.objects.get(id=obj_id)
        if action == "verify":
            if hasattr(obj, "status"):
                obj.status = "verified"
                obj.save(update_fields=["status"])
            else:
                raise AttributeError(f"{model_label} modelida 'status' maydoni yo'q")
        elif action == "cancel":
            if hasattr(obj, "status"):
                obj.status = "cancelled"
                obj.save(update_fields=["status"])
            else:
                raise AttributeError(f"{model_label} modelida 'status' maydoni yo'q")
        return f"Tranzaksiya {unique_id} {action} qilindi"
    except ObjectDoesNotExist:
        raise ValueError(f"Obyekt topilmadi: {unique_id}")
    except Exception as e:
        raise Exception(f"Xatolik yuz berdi: {str(e)}")













