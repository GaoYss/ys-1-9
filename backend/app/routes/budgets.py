from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Budget, PurchaseOrder

budgets_bp = Blueprint("budgets", __name__)


@budgets_bp.get("")
def list_budgets():
    budgets = Budget.query.order_by(Budget.month).all()
    return jsonify([b.to_dict() for b in budgets])


@budgets_bp.post("")
def create_budget():
    data = request.get_json() or {}
    budget = Budget(
        month=data["month"],
        amount=float(data["amount"]),
    )
    db.session.add(budget)
    db.session.commit()
    return budget.to_dict(), 201


@budgets_bp.put("/<int:budget_id>")
def update_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    data = request.get_json() or {}
    budget.amount = float(data.get("amount", budget.amount))
    db.session.commit()
    return budget.to_dict()


@budgets_bp.get("/dashboard")
def budget_dashboard():
    budgets = Budget.query.order_by(Budget.month).all()
    budget_map = {b.month: b.amount for b in budgets}

    orders = PurchaseOrder.query.all()
    ordered_map = {}
    for order in orders:
        if order.status == "cancelled":
            continue
        month_key = order.created_at.strftime("%Y-%m")
        ordered_map[month_key] = ordered_map.get(month_key, 0) + order.total_amount

    all_months = sorted(set(list(budget_map.keys()) + list(ordered_map.keys())))

    result = []
    for month in all_months:
        planned = budget_map.get(month, 0)
        ordered = round(ordered_map.get(month, 0), 2)
        over_budget = ordered > planned if planned > 0 else False
        result.append({
            "month": month,
            "plannedAmount": planned,
            "orderedAmount": ordered,
            "overBudget": over_budget,
            "overAmount": round(ordered - planned, 2) if over_budget else 0,
            "usageRate": round(ordered / planned * 100, 1) if planned > 0 else 0,
        })

    return jsonify(result)
