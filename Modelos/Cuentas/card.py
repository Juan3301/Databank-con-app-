from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Modelos.Cuentas.bank_account import BankAccount

import uuid
from datetime import datetime, timedelta

class Card:
    def __init__(self, account: "BankAccount", pin: str, credit_type: bool, debit_type: bool,
                 card_number: str | None = None, cvv: str | None = None,
                 expiration_date: datetime | None = None, is_blocked: bool = False):
        if credit_type and debit_type:
            raise ValueError("Una tarjeta no puede ser débito y crédito al mismo tiempo.")
        if not credit_type and not debit_type:
            raise ValueError("Una tarjeta debe ser débito o crédito.")
    
        self.card_number = card_number if card_number is not None else str(uuid.uuid4().int)[:16]
        self.cvv = cvv if cvv is not None else str(uuid.uuid4().int)[:3]
        self.__pin = pin
        self.is_blocked = is_blocked
        self.expiration_date = expiration_date if expiration_date is not None else datetime.now() + timedelta(days=365 * 4)
        self.account = account
        self.holder = account.client
        self.is_credit_card = credit_type
        self.is_debit_card = debit_type

        if self.is_credit_card:
            self.card_type = "Crédito"
        elif self.is_debit_card:
            self.card_type = "Débito"

    def __str__(self):
        return(
            f"Nombre del titular: {self.holder.name}\n"
            f"Número de tarjeta: {self.card_number}\n"
            f"Fecha de expiración: {self.expiration_date}\n"
            f"Tipo de tarjeta: {self.card_type}\n"
            f"Cuenta bancaria asociada: {self.account.account_number}"
        )
    
    def get_pin(self):
        return self.__pin
    
    def set_pin(self, current_pin: str, new_pin: str):
        if current_pin == self.get_pin():
            self.__pin = new_pin
    
    def is_expired(self):
        return datetime.now() > self.expiration_date
    
    def to_dict(self):
        return{
            "holder_name": self.holder.name,
            "card_number": self.card_number,
            "cvv": self.cvv,
            "pin": self.get_pin(),
            "expiration_date": self.expiration_date.isoformat(),
            "account_number": self.account.account_number,
            "card_type": self.card_type,
            "is_credit_card": self.is_credit_card,
            "is_debit_card": self.is_debit_card,
            "is_blocked": self.is_blocked
        }