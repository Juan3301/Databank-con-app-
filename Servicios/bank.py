import json
from datetime import datetime, timedelta
from Modelos.Cuentas.bank_account import BankAccount
from Modelos.Cuentas.checking_account import CheckingAccount
from Modelos.Cuentas.savings_account import SavingsAccount
from Modelos.Cuentas.young_account import YoungAccount
from Modelos.Cuentas.client import Client
from Modelos.Cuentas.transaction import Transaction
from Modelos.Roles.employee import Employee
from Modelos.Excepciones.impossible_operation_exception import ImpossibleOperationException
from Modelos.Log.log import Log
from Modelos.Roles.analist import Analist
from Modelos.Roles.administrative import Administrative
from Modelos.Roles.director import Director
from Modelos.Roles.logistic import Logistic
from Servicios.bonus_admin import BonusAdmin
from Servicios.analize import Analize
from Servicios.autenticate import AutenticateObjects
from Servicios.list_objects import ListObjects
from Servicios.manage_accounts import ManageAccounts
from Servicios.manage_credits import ManageCredits
from Servicios.manage_employees import ManageEmployees
from Servicios.manage_cards import ManageCards
from Servicios.notificate import Notificate
from Servicios.report import ReportObjects
from Servicios.search import SearchObjects
from Servicios.auditlog import AuditLog
from Servicios.promotion_request import PromotionRequest
from Servicios.salary_inc_req import SalaryIncreaseRequest

class Bank:
    def __init__(self, name: str, number: int, clients: list[Client], employees: list[Employee], global_transactions: list[Transaction], logs: list[Log], bonus_admin: BonusAdmin):
        self.name = name
        self.bank_number = number
        self.clients = clients
        self.employees = employees
        self.accounts: list[BankAccount] = []
        self.global_transactions = global_transactions
        self.logs = logs
        self.bonus_admin = bonus_admin
        self.interest_rate = 0.06
        self.audit_history: list[AuditLog]= []
        self.promotion_requests: list [PromotionRequest] = []
        self.salary_requests: list [SalaryIncreaseRequest] = []

        self.analize = Analize(self)
        self.autenticate = AutenticateObjects(self)
        self.list_objects = ListObjects(self)
        self.manage_accounts = ManageAccounts(self)
        self.manage_credits = ManageCredits(self)
        self.manage_employees = ManageEmployees(self)
        self.manage_cards = ManageCards(self)
        self.notificate = Notificate(self)
        self.report = ReportObjects(self)
        self.search = SearchObjects(self)

    @property
    def total_assets(self) -> float:
        return sum(account.get_balance() for account in self.accounts)

    def validate_permission(self, employee: "Employee", action: str):
        permissions = {
            "Crear_Empleado": employee.can_create_user(),
            "Eliminar_Empleado": employee.can_delete_user(),
            "Ver_informacion": employee.can_see_information(),
            "Ver_reportes": employee.can_see_reports(),
            "Cambiar_rol": employee.can_change_role,
            "Crear_Cliente": employee.can_create_user(),
            "Borrar_Cuenta": employee.can_delete_user(),
        }

        if action not in permissions:
            raise ImpossibleOperationException("Operación inválida")
        
        if not permissions[action]:
            raise PermissionError(
                f"{employee.name} no tiene permiso para {action}"
            )
        
        return True

    def create_client(self, employee: "Employee", client_data):
        self.validate_permission(employee, "Crear_Empleado")

        client = Client (
            client_data["name"],
            client_data["dni"],
            client_data["age"],
            client_data["profession"]
        )

        self.clients.append(client)
        return client

    def upgrade_client(self, employee: "Employee", client: "Client", account_type: str):
        self.validate_permission(employee, "Crear_Empleado")

        return self.manage_accounts.create_account(employee, client, account_type)


    def register_transaction(self, transaction: "Transaction"):
        self.global_transactions.append(transaction)

    def get_account_history(self, account: BankAccount):
        return account.transactions

    def get_client_history(self, client: "Client"):
        transactions = []

        for account in self.accounts:
            if account.client == client:
                for transaction in account.transactions:
                    transactions.append(transaction)

        return transactions

    def get_global_transactions(self, employee: "Employee"):
        self.validate_permission(employee, "Ver_informacion")
        return self.global_transactions

    def register_global_bonus(self):
        for employee in self.employees:
            self.bonus_admin.register(employee)

    def get_total_bonus(self):
        return self.bonus_admin.get_total_bonus()

    def sort_accounts_by_number(self):
        self.accounts.sort(key=lambda account: account.account_number)

        return self.accounts

    def sort_accounts_by_balance(self):
        self.accounts.sort(key=lambda account: account.get_balance())

        return self.accounts

    def register_log(self, action: str, employee: "Employee", status: bool, details: str):
        log = Log(employee, action, status, details)
        self.logs.append(log)
        
        return log

    def get_logs(self):
        return self.logs

    def export_accounts_json(self):
        data = []

        for account in self.accounts:
            data.append({
                "Número de cuenta": account.account_number,
                "Número de banco": account.bank_number,
                "Cliente": account.client.name,
                "Saldo": account.get_balance()
            })
        with open("accounts.json", "w") as file:
            json.dump(
                data,
                file,
                indent=4
            )
      
    def validate_transfer_limit(self, amount: float, limit: float):
        if amount <= 0:
            raise ValueError("El monto debe ser mayor a 0.")
        return amount <= limit
          
  
    def temporary_account_lock(self, account: "BankAccount", minutes: int):
        if minutes <= 0:
            raise ValueError("Los minutos deben ser mayor a 0.")
        account.account_active = False
        account.locked_until = datetime.now() + timedelta(minutes=minutes)
        return account.locked_until
  

    def blacklist_client(self, employee: "Employee", client: "Client", reason: str):
        self.validate_permission(employee, "Eliminar_Empleado")
        if not hasattr(client, "is_blacklisted"):
            client.is_blacklisted = False
        client.is_blacklisted = True
        client.blacklist_reason = reason
        self.register_log("Cliente en lista negra", employee, True, f"Cliente {client.name} (DNI: {client.dni}) bloqueado. Motivo: {reason}")
        return True
    
    def register_log_e(self, log_entry):
        self.audit_history.append(log_entry)

        try:
            log_data = {
                "timestamp": log_entry.timestamp,
                "action_type": log_entry.action_type,
                "operator_name": log_entry.operator_name,
                "target_name": log_entry.target_name,
                "target_dni": log_entry.target_dni,
                "details": log_entry.details
            }
            
            try:
                with open("audit_history.json", "r", encoding="utf-8") as file:
                    history = json.load(file)
            except FileNotFoundError:
                history = []
                
            history.append(log_data)
            
            with open("audit_history.json", "w", encoding="utf-8") as file:
                json.dump(history, file, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error al escribir log en archivo: {e}")
    
    def export_data_json(self):
        data = {
            "bank_name": self.name,
            "bank_number": self.bank_number,
            "interest_rate": self.interest_rate,
            "clients": [client.to_dict() for client in self.clients],
            "employees": [employee.to_dict() for employee in self.employees],
            "accounts": [account.to_dict() for account in self.accounts],
            "transactions": [t.to_dict() for t in self.global_transactions],
            "logs": [log.to_dict() for log in self.logs]
        }

        with open(f"{self.name}_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False) #aquí el ensure_ascii=False hace que caracteres como ñ o los acentos se guarden, al igual que encoding="utf-8". Recuerden el próximos usos.

        return True
    
    def import_data_json(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.name = data["bank_name"]
        self.bank_number = data["bank_number"]
        self.interest_rate = data["interest_rate"]

        clients_by_dni = {}
        self.clients = []
        for c in data["clients"]:
            client = Client(c["name"], c["dni"], c["age"], c["profession"])
            client.is_blacklisted = c["is_blacklisted"]
            client.blacklist_reason = c["blacklist_reason"]
            clients_by_dni[c["dni"]] = client
            self.clients.append(client)

        self.employees = []
        for e in data["employees"]:
            t = e["employee_type"]
            if t == "Director":
                emp : Employee = Director(e["name"], e["dni"], e["department"], e["experience"], e["password"])
            elif t == "Administrative":
                emp = Administrative(e["name"], e["dni"], e["experience"], e["password"])
            elif t == "Analist":
                emp = Analist(e["name"], e["dni"], e["experience"], e["password"])
            elif t == "Logistic":
                emp = Logistic(e["name"], e["dni"], e["experience"], e["password"])
            else:
                continue
            emp.is_blocked = e["is_blocked"]
            emp.failed_attempts = e["failed_attempts"]
            emp.can_change_role = e["can_change_role"]
            self.employees.append(emp)

        self.accounts = []
        for a in data["accounts"]:
            client = clients_by_dni[a["client_dni"]]
            t = a["account_type"]
            if t == "SavingsAccount":
                acc: BankAccount = SavingsAccount(a["bank_number"], client, a["account_number"])
            elif t == "CheckingAccount":
                acc = CheckingAccount(a["bank_number"], client, a["account_number"])
            elif t == "YoungAccount":
                acc = YoungAccount(a["bank_number"], client, a["account_number"])
            else:
                continue  # BussinessAccount se salta por el bug mencionado
            acc._balance = a["balance"]
            acc.interest_rate = a["interest_rate"]
            acc.overdraft_limit = a["overdraft_limit"]
            acc.account_active = a["account_active"]
            acc.commission_value = a["commission_value"]
            if a["locked_until"]:
                acc.locked_until = datetime.fromisoformat(a["locked_until"])
            self.accounts.append(acc)

        from Modelos.Cuentas.credit import Credit
        for c in data["clients"]:
            client = clients_by_dni[c["dni"]]
            for cr in c["credits"]:
                credit = Credit(cr["amount"], cr["interest_rate"], cr["months"], client)
                credit.approved = cr["approved"]
                credit.remaining_balance = cr["remaining_balance"]
                credit.status = cr["status"]
                
        self.logs = []

        return True
        
