from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Servicios.bank import Bank

from Modelos.Cuentas.bank_account import BankAccount
from Modelos.Cuentas.card import Card
from Modelos.Excepciones.impossible_operation_exception import ImpossibleOperationException

class ManageCards:
    def __init__(self, bank: "Bank"):
        self.bank = bank

    def create_card(self, account: BankAccount, pin: str, credit: bool, debit: bool):
          if account not in self.bank.accounts:
            raise ImpossibleOperationException("La cuenta no existe en el banco.")
          card = Card(account, pin, credit, debit)
          account.cards.append(card)
          print(f"Se ha creado la tarjeta {card.card_number} a nombre de {card.holder}")
          return card
  
    def block_card(self, card: "Card"):
        card.is_blocked = True
        print(f"Se ha bloqueado la tarjeta {card.card_number} a nombre de {card.holder}")
  
    def unblock_card(self, card):
        card.is_blocked = False
        print(f"Se ha desbloqueado la tarjeta {card.card_number} a nombre de {card.holder}")
  
    def validate_card(self, card: "Card"):
          if card.is_blocked:
              return False
          elif card.is_expired():
              return False
          else: 
              return True
          
    def change_card_pin(self, card: "Card", current_pin: str, new_pin: str):
        card.set_pin(current_pin, new_pin)
        print(f"Se ha cambiado el pin de la tarjeta {card.card_number} a nombre de {card.holder}")