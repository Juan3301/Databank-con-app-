from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Servicios.bank import Bank

from Modelos.Cuentas.client import Client
from Modelos.Roles.employee import Employee


class ListObjects:
    def __init__(self, bank: "Bank"):
        self.bank = bank

    def list_client(self, employee: "Employee"):
        self.bank.validate_permission(employee, "Ver_informacion")

        return self.bank.clients
    
    def list_accounts(self, employee: "Employee"):
        self.bank.validate_permission(employee, "Ver_informacion")
        print ("======== Listado de cuentas ========")

        return self.bank.accounts

    def list_accounts_by_client(self, client: "Client"):
        accounts = []

        for account in self.bank.accounts:
            if account.client == client:
                accounts.append(account)
        print (f"======== Listado de cuentas del cliente {client.name} ========")
        return accounts

    def list_accounts_by_bank(self, new_bank_number: int):
        accounts = []

        for account in self.bank.accounts:
            if account.bank_number == new_bank_number:
                accounts.append(account)
        print (f"======== Listado de cuentas por banco no. {new_bank_number}========")
        return accounts

    def list_employees(self, employee: "Employee"):
        self.bank.validate_permission(employee, "Ver_informacion")
        
        print ("\n======== Listado de empleados ========")
        return self.bank.employees
    
    def list_active_credits(self):
          active_credits = []
          for client in self.bank.clients:
              for credit in client.credits:
                  if credit.status == "Aprobado":
                      active_credits.append(credit)
          print ("\n======== Listado de créditos activos ========")
          return active_credits
    
    def list_cards(self):
        cards = []
        for account in self.bank.accounts:
            for card in account.cards:
                cards.append(card)
        print ("\n======== Listado de tarjetas ========")
        return cards
    
    def list_cards_by_client(self, client: "Client"):
        cards = []
        for account in self.bank.accounts:
            if account.client == client:
                for card in account.cards:
                    cards.append(card)
        print (f"======== Listado de tarjetas del cliente: {client.name} ========")
        return cards
        
    
    
