from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Servicios.bank import Bank

from Modelos.Cuentas.client import Client
from Modelos.Cuentas.savings_account import SavingsAccount
from Modelos.Cuentas.checking_account import CheckingAccount
from Modelos.Cuentas.business_account import BussinessAccount
from Modelos.Cuentas.young_account import YoungAccount
from Modelos.Roles.employee import Employee

class Analize:
    def __init__(self, bank: "Bank"):
        self.bank = bank

    def get_total_bank_money(self):
          total_money = 0
          for account in self.bank.accounts:
              total_money += account.get_balance()
          return total_money
    
    def get_total_transactions(self):
        total = 0
        for account in self.bank.accounts:
            total += len(account.transactions)
        return total

    def detect_suspicious_operations(self):
        suspicious_accounts = []

        for account in self.bank.accounts:
            if (account.get_withdrawals_without_balance() >= 3):
                suspicious_accounts.append(account)

        return suspicious_accounts
    
    def get_most_used_account_type(self):
        if not self.bank.accounts:
            return None
        
        ahorros = 0
        corriente = 0
        empresarial = 0
        juvenil = 0

        for account in self.bank.accounts:
            if isinstance(account, SavingsAccount):
                ahorros += 1
            elif isinstance(account, CheckingAccount):
                corriente += 1
            elif isinstance(account, BussinessAccount):
                empresarial += 1
            elif isinstance(account, YoungAccount):
                juvenil += 1

        if ahorros >= corriente and ahorros >= empresarial and ahorros >= juvenil:
            return "SavingsAccount"
        elif corriente >= empresarial and corriente >= juvenil:
            return "CheckingAccount"
        elif empresarial >= juvenil:
            return "BussinessAccount"
        else:
            return "YoungAccount"
    
    def get_top_clients(self, n: int):
        if n <= 0:
            raise ValueError("n debe ser mayor a 0.")
        client_balances = []
        for client in self.bank.clients:
            total = sum(
                account.get_balance()
                for account in self.bank.accounts
                if account.client == client
            )
            client_balances.append((client, total))
        client_balances.sort(key=lambda x: x[1], reverse=True)
        return [client for client, _ in client_balances[:n]]
    
    def classify_client(self, client: "Client"):
        total_balance = sum(
            account.get_balance()
            for account in self.bank.accounts
            if account.client == client
        )
        if total_balance >= 100000:
            return "VIP"
        elif total_balance >= 10000:
            return "Preferencial"
        else:
            return "Básico"
          
    def calculate_client_score(self, client: "Client"):
        score = 0.0
        total_balance = 0.0
            
        for account in self.bank.accounts:
              if account.client == client:
                  total_balance += account.get_balance()

        if total_balance/1000 < 300:
          score += total_balance/1000
        else:
          score +=300

        paid_credits = [c for c in client.credits if c.status == "Pagado"]
        score += len(paid_credits) * 50

        rejected_credits = [c for c in client.credits if c.status == "Rechazado"]
        score -= len(rejected_credits) * 30

        if score < 0:
            return 0

        return round(score)
  
    def currency_conversion(self, amount: float, from_currency: str, to_currency: str, rates: dict):
          # Convierte un monto entre monedas usando un diccionario de tasas respecto al USD.
          if from_currency not in rates or to_currency not in rates:
              raise ValueError(f"Moneda no soportada. Disponibles: {list(rates.keys())}")
          if amount <= 0:
              raise ValueError("El monto debe ser mayor a 0.")
          amount_in_base = amount / rates[from_currency]
          converted = amount_in_base * rates[to_currency]
          return round(converted, 2)
    
    def detect_large_transactions(self, limit: float):
        large_transactions = []

        for transaction in self.bank.global_transactions:
            if transaction.amount > limit:
                large_transactions.append(transaction)

        return large_transactions
    
    def detect_suspicious_logins(self,employee: "Employee"):
        return employee.failed_attempts >=3