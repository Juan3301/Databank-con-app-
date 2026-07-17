from Modelos.Cuentas.bank_account import BankAccount
from Modelos.Excepciones.impossible_operation_exception import ImpossibleOperationException
from Modelos.Cuentas.client import Client

class CheckingAccount(BankAccount):
    def __init__(self, bank_number: int, client: Client, account_number: int | None = None):
        super().__init__(bank_number, client, account_number)
        self.overdraft_limit = -500
    
    def get_min_balance(self):
        return self.overdraft_limit
    
    def withdraw(self, amount: float) -> bool:
        if amount <=0:
            raise ImpossibleOperationException("Monto Inválido")
        
        if self.get_balance() - amount < self.overdraft_limit:
            raise ImpossibleOperationException("Límite de sobregiro excedido")
        
        return super().withdraw(amount)
    
    def get_max_transactions_per_minute(self):
        return 15
    
    def can_withdraw(self, amount):
        return self._balance - amount >= self.get_min_balance()