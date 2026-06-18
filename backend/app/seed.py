from datetime import date

from .extensions import db
from .models import Budget, Ingredient, PurchaseOrder, PurchaseOrderItem, StockRecord, Supplier


def seed_data():
    if Supplier.query.first():
        return

    suppliers = [
        Supplier(
            name="香叶原料供应链",
            contact="林经理",
            phone="13800010001",
            address="杭州市余杭区良渚仓配园",
            rating=5,
        ),
        Supplier(
            name="甜蜜乳品配送",
            contact="周主管",
            phone="13800010002",
            address="上海市闵行区冷链中心",
            rating=4,
        ),
        Supplier(
            name="果然鲜果业",
            contact="陈女士",
            phone="13800010003",
            address="广州市白云区水果批发市场",
            rating=4,
        ),
    ]
    db.session.add_all(suppliers)
    db.session.flush()

    ingredients = [
        Ingredient(
            name="阿萨姆红茶",
            category="茶叶",
            unit="kg",
            stock=28,
            warning_threshold=20,
            supplier_id=suppliers[0].id,
        ),
        Ingredient(
            name="茉莉绿茶",
            category="茶叶",
            unit="kg",
            stock=12,
            warning_threshold=18,
            supplier_id=suppliers[0].id,
        ),
        Ingredient(
            name="鲜牛奶",
            category="乳制品",
            unit="L",
            stock=65,
            warning_threshold=50,
            supplier_id=suppliers[1].id,
        ),
        Ingredient(
            name="黑糖珍珠",
            category="小料",
            unit="kg",
            stock=9,
            warning_threshold=15,
            supplier_id=suppliers[1].id,
        ),
        Ingredient(
            name="芒果果浆",
            category="果浆",
            unit="瓶",
            stock=34,
            warning_threshold=24,
            supplier_id=suppliers[2].id,
        ),
    ]
    db.session.add_all(ingredients)
    db.session.flush()

    budgets = [
        Budget(month="2026-01", amount=8000),
        Budget(month="2026-02", amount=12000),
        Budget(month="2026-03", amount=6000),
        Budget(month="2026-04", amount=16000),
        Budget(month="2026-05", amount=12000),
        Budget(month="2026-06", amount=22000),
    ]
    db.session.add_all(budgets)

    from datetime import datetime

    order_jan_1 = PurchaseOrder(
        order_no="PO20260105001",
        supplier_id=suppliers[0].id,
        status="received",
        expected_date=date(2026, 1, 12),
        remark="年初茶叶备货",
        created_at=datetime(2026, 1, 5),
    )
    order_jan_1.items = [
        PurchaseOrderItem(ingredient_id=ingredients[0].id, quantity=40, unit_price=46),
        PurchaseOrderItem(ingredient_id=ingredients[1].id, quantity=30, unit_price=52),
    ]
    db.session.add(order_jan_1)

    order_jan_2 = PurchaseOrder(
        order_no="PO20260118001",
        supplier_id=suppliers[1].id,
        status="received",
        expected_date=date(2026, 1, 25),
        remark="乳品周常补货",
        created_at=datetime(2026, 1, 18),
    )
    order_jan_2.items = [
        PurchaseOrderItem(ingredient_id=ingredients[2].id, quantity=80, unit_price=12),
        PurchaseOrderItem(ingredient_id=ingredients[3].id, quantity=20, unit_price=35),
    ]
    db.session.add(order_jan_2)

    order_feb_1 = PurchaseOrder(
        order_no="PO20260210001",
        supplier_id=suppliers[2].id,
        status="received",
        expected_date=date(2026, 2, 15),
        remark="果浆补货",
        created_at=datetime(2026, 2, 10),
    )
    order_feb_1.items = [
        PurchaseOrderItem(ingredient_id=ingredients[4].id, quantity=50, unit_price=68),
    ]
    db.session.add(order_feb_1)

    order_feb_2 = PurchaseOrder(
        order_no="PO20260220001",
        supplier_id=suppliers[1].id,
        status="cancelled",
        expected_date=date(2026, 2, 28),
        remark="临时取消-供应商缺货",
        created_at=datetime(2026, 2, 20),
    )
    order_feb_2.items = [
        PurchaseOrderItem(ingredient_id=ingredients[2].id, quantity=100, unit_price=12),
    ]
    db.session.add(order_feb_2)

    order_mar_1 = PurchaseOrder(
        order_no="PO20260305001",
        supplier_id=suppliers[0].id,
        status="received",
        expected_date=date(2026, 3, 12),
        remark="春季茶品备货",
        created_at=datetime(2026, 3, 5),
    )
    order_mar_1.items = [
        PurchaseOrderItem(ingredient_id=ingredients[0].id, quantity=50, unit_price=46),
        PurchaseOrderItem(ingredient_id=ingredients[1].id, quantity=40, unit_price=52),
    ]
    db.session.add(order_mar_1)

    order_mar_2 = PurchaseOrder(
        order_no="PO20260315001",
        supplier_id=suppliers[1].id,
        status="received",
        expected_date=date(2026, 3, 22),
        remark="乳制品批量采购",
        created_at=datetime(2026, 3, 15),
    )
    order_mar_2.items = [
        PurchaseOrderItem(ingredient_id=ingredients[2].id, quantity=120, unit_price=12),
        PurchaseOrderItem(ingredient_id=ingredients[3].id, quantity=35, unit_price=35),
    ]
    db.session.add(order_mar_2)

    order_mar_3 = PurchaseOrder(
        order_no="PO20260325001",
        supplier_id=suppliers[2].id,
        status="cancelled",
        expected_date=date(2026, 4, 1),
        remark="取消-改用其他供应商",
        created_at=datetime(2026, 3, 25),
    )
    order_mar_3.items = [
        PurchaseOrderItem(ingredient_id=ingredients[4].id, quantity=60, unit_price=68),
    ]
    db.session.add(order_mar_3)

    order_apr_1 = PurchaseOrder(
        order_no="PO20260408001",
        supplier_id=suppliers[0].id,
        status="approved",
        expected_date=date(2026, 4, 15),
        remark="谷雨茶补货",
        created_at=datetime(2026, 4, 8),
    )
    order_apr_1.items = [
        PurchaseOrderItem(ingredient_id=ingredients[0].id, quantity=35, unit_price=46),
    ]
    db.session.add(order_apr_1)

    order_apr_2 = PurchaseOrder(
        order_no="PO20260420001",
        supplier_id=suppliers[1].id,
        status="approved",
        expected_date=date(2026, 4, 28),
        remark="五一备货-乳品",
        created_at=datetime(2026, 4, 20),
    )
    order_apr_2.items = [
        PurchaseOrderItem(ingredient_id=ingredients[2].id, quantity=90, unit_price=12),
        PurchaseOrderItem(ingredient_id=ingredients[3].id, quantity=25, unit_price=35),
    ]
    db.session.add(order_apr_2)

    order_may_1 = PurchaseOrder(
        order_no="PO20260505001",
        supplier_id=suppliers[2].id,
        status="approved",
        expected_date=date(2026, 5, 12),
        remark="夏日果浆大量采购",
        created_at=datetime(2026, 5, 5),
    )
    order_may_1.items = [
        PurchaseOrderItem(ingredient_id=ingredients[4].id, quantity=120, unit_price=68),
    ]
    db.session.add(order_may_1)

    order_may_2 = PurchaseOrder(
        order_no="PO20260518001",
        supplier_id=suppliers[0].id,
        status="approved",
        expected_date=date(2026, 5, 25),
        remark="茶叶追加采购",
        created_at=datetime(2026, 5, 18),
    )
    order_may_2.items = [
        PurchaseOrderItem(ingredient_id=ingredients[0].id, quantity=60, unit_price=46),
        PurchaseOrderItem(ingredient_id=ingredients[1].id, quantity=45, unit_price=52),
    ]
    db.session.add(order_may_2)

    order_jun_1 = PurchaseOrder(
        order_no="PO20260605001",
        supplier_id=suppliers[1].id,
        status="approved",
        expected_date=date(2026, 6, 12),
        remark="六月乳品补货",
        created_at=datetime(2026, 6, 5),
    )
    order_jun_1.items = [
        PurchaseOrderItem(ingredient_id=ingredients[2].id, quantity=100, unit_price=12),
        PurchaseOrderItem(ingredient_id=ingredients[3].id, quantity=30, unit_price=35),
    ]
    db.session.add(order_jun_1)

    order_jun_2 = PurchaseOrder(
        order_no="PO20260611001",
        supplier_id=suppliers[0].id,
        status="approved",
        expected_date=date(2026, 6, 18),
        remark="补充茶叶安全库存",
        created_at=datetime(2026, 6, 11),
    )
    order_jun_2.items = [
        PurchaseOrderItem(ingredient_id=ingredients[0].id, quantity=30, unit_price=46),
        PurchaseOrderItem(ingredient_id=ingredients[1].id, quantity=25, unit_price=52),
    ]
    db.session.add(order_jun_2)

    order_jun_3 = PurchaseOrder(
        order_no="PO20260615001",
        supplier_id=suppliers[2].id,
        status="cancelled",
        expected_date=date(2026, 6, 22),
        remark="取消-预算调整",
        created_at=datetime(2026, 6, 15),
    )
    order_jun_3.items = [
        PurchaseOrderItem(ingredient_id=ingredients[4].id, quantity=80, unit_price=68),
    ]
    db.session.add(order_jun_3)

    db.session.add_all(
        [
            StockRecord(
                ingredient_id=ingredients[2].id,
                record_type="in",
                quantity=40,
                operator="王店长",
                source="采购入库",
                note="每日乳品补货",
            ),
            StockRecord(
                ingredient_id=ingredients[3].id,
                record_type="out",
                quantity=6,
                operator="李班长",
                source="门店领用",
                note="晚班备料",
            ),
        ]
    )
    db.session.commit()
