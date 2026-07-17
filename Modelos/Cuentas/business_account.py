from Modelos.Cuentas.bank_account import BankAccount
from Modelos.Cuentas.client import Client

class BussinessAccount(BankAccount):
    def __init__(self, bank_number: int, client: Client, nit: int, authorized_users: list["Client"], account_number: int | None = None):
        super().__init__(bank_number, client, account_number)
        self.nit = nit
        self.authorized_users = authorized_users
        self.overdraft_limit = -10000
        self.daily_withdrawal_limit = 100
    
    def add_authorized_user(self, new_user: "Client"):
        self.authorized_users.append(new_user)
    
    def get_max_transactions_per_minute(self):
        return 10
    
    def can_withdraw(self, amount):
        return (
            len(self.daily_withdraws()) < self.daily_withdrawal_limit
            and self._balance - amount >= 0
        )    
    
    def to_dict(self):
        data = super().to_dict()
        data["nit"] = self.nit
        data["daily_withdrawal_limit"] = self.daily_withdrawal_limit
        data["authorized_users"] = [user.dni for user in self.authorized_users]
        return data

