from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Servicios.bank import Bank

from Modelos.Cuentas.credit import Credit
from Modelos.Cuentas.client import Client
from Modelos.Roles.employee import Employee
from Modelos.Excepciones.impossible_operation_exception import ImpossibleOperationException

class ManageCredits:
    def __init__(self, bank: "Bank"):
        self.bank = bank

    def request_credit(self, client: Client, amount: float, months: int):
        # El constructor de Credit ya se registra a sí mismo en client.credits
        #(client.add_credit(self)) entonces aquí no hay que volver a agregarlo.
        credit = Credit(amount, self.bank.interest_rate, months, client)

        return credit

    def approve_credit(self, employee: "Employee", client: Client, credit: Credit):
        if not employee.can_approve_credit(credit.amount):
            raise ImpossibleOperationException("El empleado no tiene permisos para aprobar créditos.")
        
        if credit not in client.credits:
            raise ImpossibleOperationException("El crédito no pertenece a este cliente.")
            
        if credit.status != "Pendiente":
            raise ImpossibleOperationException("Sólo se pueden aprobar créditos pendientes.")
            
        credit.approved = True
        credit.status = "Aprobado"

        return True
    
    def reject_credit(self, client: "Client", credit: "Credit"):
        if credit not in client.credits:
            raise ValueError("El crédito no pertenece a este cliente")
        
        if credit.status != "Pendiente":
            raise ImpossibleOperationException("Sólo se pueden rechazar créditos pendientes")
        
        if client.age > 65:
            credit.approved = False
            credit.status = "Rechazado"
            return "El cliente supera la edad máxima, el crédito ha sido rechazado."
        
        active = []
        for cred in client.credits:
            if cred.status == "Aprobado":
                active.append(cred)
                
        if active:
            credit.approved = False
            credit.status = "Rechazado"
            return "El cliente ya tiene un crédito aprobado, no puede solicitar otro."
        
        pending = []
        for cred in client.credits:
            if cred == credit:
                continue

            if cred.remaining_balance > 0 and cred.status != "Rechazado":
                pending.append(cred)

        if pending:
            credit.approved = False
            credit.status = "Rechazado"
            return "El cliente tiene cuotas pendientes. Solicitud de crédito rechazada."
        
        client_accounts = []
        for acc in self.bank.accounts:
            if acc.client == client:
                client_accounts.append(acc)

        found = False
        for acc in client_accounts:
            if acc.get_balance() < 0:
                found = True
                break
        if found:
            credit.approved = False
            credit.status = "Rechazado"
            return "El cliente tiene saldo negativo en alguna cuenta. Crédito denegado."
        
        raise ImpossibleOperationException ("No hay motivo para rechazar el crédito")

 
    def calculate_credit_interest(self, credit: "Credit"):
        return credit.amount * credit.interest_rate * (credit.months / 12)
    
    def calculate_monthly_installment(self, credit : "Credit"):
        return (credit.amount + self.calculate_credit_interest(credit))/credit.months

    def pay_credit_installment(self, client: "Client", credit: "Credit", amount: float):
        if credit not in client.credits:
            raise ValueError("El crédito no pertenece a este cliente.")
   
        if credit.status != "Aprobado":
            raise ImpossibleOperationException("El crédito no está activo.")
   
        if amount <= 0:
            raise ValueError("El monto de la cuota debe ser mayor a 0.")
   
        if amount > credit.remaining_balance:
            amount = credit.remaining_balance
   
        credit.remaining_balance -= amount
   
        if credit.remaining_balance <= 0:
            credit.remaining_balance = 0
            credit.status = "Pagado"
   
        return credit.remaining_balance
      