from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Servicios.bank import Bank
    
from Modelos.Roles.autenticatable_employee import AutenticatableEmployee
from Modelos.Roles.employee import Employee
from Modelos.Roles.director import Director
from Modelos.Roles.administrative import Administrative
from Modelos.Roles.analist import Analist
from Modelos.Roles.logistic import Logistic
from Modelos.Excepciones.impossible_operation_exception import ImpossibleOperationException
class ManageEmployees:
    def __init__(self, bank: "Bank"):
        self.bank = bank
    
    def add_employee(self, employee: "Employee", target: "Employee"):
        self.bank.validate_permission(employee, "Crear_Empleado")
        if any(e.get_dni() == target.get_dni() for e in self.bank.employees):
            raise ImpossibleOperationException(f"Ya existe un empleado registrado con el DNI {target.get_dni()}.")
        self.bank.employees.append(target)
        print("\nEmpleado añadido exitosamente.")
        return target

    def delete_employee(self, employee: "Employee", target: "Employee"):
        self.bank.validate_permission(employee, "Eliminar_Empleado")
        if target in self.bank.employees: 
            self.bank.employees.remove(target) 
            print("\nEmpleado removido exitosamente.")
            return True 
        return False

    def change_role(self, employee: "AutenticatableEmployee", target: "AutenticatableEmployee", new_role: str, department: str):
        self.bank.validate_permission(employee, "Crear_Empleado")

        if target not in self.bank.employees:
            raise ImpossibleOperationException("El empleado objetivo no pertenece a este banco.")

        if new_role == "Analista":
            new_employee : Employee = Analist(target.name, target.get_dni(), target.experience, target.get_password())
            print("\nCambio a analista realizado exitosamente.")
        
        elif new_role == "Logistica":
            new_employee = Logistic(target.name, target.get_dni(), target.experience, target.get_password())
            print("\nCambio a logistica realizado exitosamente.")
        
        elif new_role == "Administrativo":
            new_employee = Administrative(target.name, target.get_dni(), target.experience, target.get_password())
            print("\nCambio a administrativo realizado exitosamente.")
        
        elif new_role == "Director":
            new_employee = Director(target.name, target.get_dni(), department, target.experience, target.get_password())
            print("\nCambio a director realizado exitosamente.")
        
        else:
            raise ImpossibleOperationException("Rol inválido.")

        self.bank.employees[self.bank.employees.index(target)] = new_employee
        return new_employee

    def approve_salary_increase(self, employee: "Employee", target, amount: float):
        if not employee.can_modify_salary(target, amount):
            raise PermissionError("No es posible modificar el salario.")

        target.set_salary(target.get_salary() + amount)

        return target.get_salary()


    def apply_salary_increase(self, employee: "Employee", target: "Employee"):
        if not employee.can_raise_salary(target):
            raise PermissionError("No es posible aumentar el salario.")
        
        target.raise_salary()

        return target.get_salary()

    def evaluate_promotion(self, director: "Director", employee: "Employee"):
        if not director.can_create_user():
            raise ImpossibleOperationException("Permiso denegado.")
        
        if employee.can_request_promotion():
            return {
                "eligible": True,
                "reason": "El empleado cumple los requisitos mínimos para solicitar promoción."
            }
        
        return {
            "eligible": False,
            "reason": "El empleado no cumple todos los requisitos para ser promovido."
        }
    
    def approve_promotion(self, director: "Director", employee: "Employee"):
        if not director.can_create_user():
            raise ImpossibleOperationException("Permiso denegado.")

        employee.experience += 1

        return True
    
    def update_experience(self, employee: "Employee", points: int):
        employee.experience += points

        return employee.experience
    

