from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Servicios.bank import Bank
    
from Modelos.Roles.autenticatable_employee import AutenticatableEmployee
from Modelos.Roles.employee import Employee

class AutenticateObjects:
    def __init__(self, bank: "Bank"):
        self.bank = bank
    
    def autenticate_user(self, employee: "AutenticatableEmployee", password: str):
        if employee.authenticate_user(password):
            return True

        self.verify_failed_attempt(employee)
        return False
    
    def verify_failed_attempt(self, employee: "Employee"):
        employee.failed_attempts +=1

        if employee.failed_attempts >= 3:
            self.block_employee(employee)

    def block_employee(self, employee: "Employee"):
        employee.is_blocked= True


    def unblock_employee(self, employee: "Employee"):
        employee.is_blocked = False
        employee.failed_attempts = 0

        def suspicious_login_detection(self):
          if self.employee_login_history() > 3:
              return True
          elif self.password_attempts() > 3:
              return True
          elif self.unusual_location_login():
              return True
          elif self.password_change_history() > 3:
              return True
          elif self.password != self.password:
              return True