from Modelos.Cuentas.bank_account import BankAccount
from Modelos.Cuentas.client import Client
from Modelos.Excepciones.impossible_operation_exception import ImpossibleOperationException

class YoungAccount(BankAccount):
    def __init__(self, bank_number: int, client: Client, account_number: int | None = None):
        if not (13<= client.age <=20):
            raise ImpossibleOperationException("Sólo clientes entre 13 y 20 años pueden tener una cuenta juvenil.")
        
        super().__init__(bank_number, client, account_number)
        self.daily_withdrawal_limit = 5
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit
            and self._balance - amount >= 0
        )    
    
    def to_dict(self):
        data = super().to_dict()
        data["daily_withdrawal_limit"] = self.daily_withdrawal_limit
        return data
