from Modelos.Cuentas.client import Client

class Credit:
    def __init__(self, amount: float, interest_rate: float, months: int, client: Client):
        self.amount = amount
        self.interest_rate = interest_rate
        self.months = months
        self.client = client
        self.approved = False
        self.remaining_balance = amount
        self.status = "Pendiente"
        client.add_credit(self)

    def __str__(self) -> str:
        return (f"Credito de {self.amount} para {self.client.name}")
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "interest_rate": self.interest_rate,
            "months": self.months,
            "approved": self.approved,
            "remaining_balance": self.remaining_balance,
            "status": self.status
        }
