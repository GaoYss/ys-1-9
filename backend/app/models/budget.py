from ..extensions import db


class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(7), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "month": self.month,
            "amount": self.amount,
        }
