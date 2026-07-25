import json
from datetime import datetime, timedelta
from Modelos.Cuentas.bank_account import BankAccount
from Modelos.Cuentas.checking_account import CheckingAccount
from Modelos.Cuentas.savings_account import SavingsAccount
from Modelos.Cuentas.young_account import YoungAccount
from Modelos.Cuentas.business_account import BussinessAccount
from Modelos.Cuentas.card import Card
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
    # La auditoría se guarda en memoria y queda cubierta por
    # export_data_json()/import_data_json() 
        self.audit_history.append(log_entry)
    
    def _collect_all_transactions(self):
        """
        Reúne todas las transacciones del banco en un solo listado sin duplicados.
        Se usa esto en vez de depender únicamente de self.global_transactions porque
        withdraw/deposit/transfer nunca llaman a register_transaction, así que esa
        lista se queda vacía; las transacciones reales solo viven dentro de cada cuenta.
        """
        all_transactions = {t.id: t for t in self.global_transactions}
        for account in self.accounts:
            for t in account.transactions:
                all_transactions[t.id] = t
        return sorted(all_transactions.values(), key=lambda t: t.date)

    def export_data_json(self, filepath: str | None = None):
        filepath = filepath or f"{self.name}_data.json"
        
        data = {
            "bank_name": self.name,
            "bank_number": self.bank_number,
            "interest_rate": self.interest_rate,
            "total_bonus": self.bonus_admin.get_total_bonus(),
            "clients": [client.to_dict() for client in self.clients],
            "employees": [employee.to_dict() for employee in self.employees],
            "accounts": [account.to_dict() for account in self.accounts],
            "transactions": [t.to_dict() for t in self._collect_all_transactions()],
            "logs": [log.to_dict() for log in self.logs],
            "audit_history": [a.to_dict() for a in self.audit_history],
            "promotion_requests": [r.to_dict() for r in self.promotion_requests],
            "salary_requests": [r.to_dict() for r in self.salary_requests],
        }

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False) #aquí el ensure_ascii=False hace que caracteres como ñ o los acentos se guarden, al igual que encoding="utf-8". Recuerden el próximos usos.

        return True
    
    def import_data_json(self, filepath: str | None = None):
        """
        Carga el estado guardado en un JSON exportado con export_data_json y lo
        SUMA al estado que ya existe en memoria. Cada entidad
        se identifica por una llave única (dni, número de cuenta, id...) para
        que si un registro ya está cargado no se duplique al volver a importar.
        """
        filepath = filepath or f"{self.name}_data.json"

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return False

        # Solo se sincronizan estos datos generales del banco si aún no hay nada cargado,
        # para que no se pisen cambios que ya se hayan hecho en la sesión actual.
        if not self.clients and not self.employees and not self.accounts:
            self.name = data["bank_name"]
            self.bank_number = data["bank_number"]
            self.interest_rate = data["interest_rate"]

        # Tema clientes
        clients_by_dni = {c.dni: c for c in self.clients}
        for c in data["clients"]:
            if c["dni"] not in clients_by_dni:
                client = Client(c["name"], c["dni"], c["age"], c["profession"])
                client.is_blacklisted = c["is_blacklisted"]
                client.blacklist_reason = c["blacklist_reason"]
                clients_by_dni[c["dni"]] = client
                self.clients.append(client)

        # Créditos de cada cliente 
        from Modelos.Cuentas.credit import Credit
        for c in data["clients"]:
            client = clients_by_dni[c["dni"]]
            existing_credit_ids = {cr.id for cr in client.credits if hasattr(cr, "id")}
            for cr in c["credits"]:
                if cr.get("id") in existing_credit_ids:
                    continue
                credit = Credit(
                    cr["amount"], cr["interest_rate"], cr["months"], client,
                    id=cr.get("id"),
                    request_date=datetime.fromisoformat(cr["request_date"]) if cr.get("request_date") else None
                )
                credit.approved = cr["approved"]
                credit.remaining_balance = cr["remaining_balance"]
                credit.status = cr["status"]

        # Tema empleados
        employees_by_dni = {e.get_dni(): e for e in self.employees}
        for e in data["employees"]:
            if e["dni"] in employees_by_dni:
                continue
            t = e["employee_type"]
            if t == "Director":
                emp: Employee = Director(e["name"], e["dni"], e["department"], e["experience"], e["password"])
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
            if e.get("locked_until"):
                emp.locked_until = datetime.fromisoformat(e["locked_until"])
            if e.get("register_date"):
                emp.register_date = datetime.fromisoformat(e["register_date"])
            employees_by_dni[e["dni"]] = emp
            self.employees.append(emp)

        # Tema Cuentas 
        accounts_by_number = {a.account_number: a for a in self.accounts}
        all_transactions_by_id = {t.id: t for t in self.global_transactions}
        
        for a in data["accounts"]:
            if a["account_number"] in accounts_by_number:
                continue
            
            client = clients_by_dni[a["client_dni"]]
            t = a["account_type"]
            
            if t == "SavingsAccount":
                acc: BankAccount = SavingsAccount(a["bank_number"], client, a["account_number"])
            elif t == "CheckingAccount":
                acc = CheckingAccount(a["bank_number"], client, a["account_number"])
            elif t == "YoungAccount":
                acc = YoungAccount(a["bank_number"], client, a["account_number"])
            elif t == "BussinessAccount":
                authorized_users = [
                    clients_by_dni[dni] for dni in a.get("authorized_users", [])
                    if dni in clients_by_dni
                ]
                acc = BussinessAccount(a["bank_number"], client, a["nit"], authorized_users, a["account_number"])
            else:
                continue 
            
            acc._balance = a["balance"]
            acc.interest_rate = a["interest_rate"]
            acc.overdraft_limit = a["overdraft_limit"]
            acc.account_active = a["account_active"]
            acc.commission_value = a["commission_value"]
            if a.get("creation_date"):
                acc.creation_date = datetime.fromisoformat(a["creation_date"])
            if a["locked_until"]:
                acc.locked_until = datetime.fromisoformat(a["locked_until"])
            
            accounts_by_number[acc.account_number] = acc
            self.accounts.append(acc)

        # viene segunda pasaya ya que ahora que todas las cuentas nuevas existen, se reconstruyen
        # sus transacciones y tarjetas (una transferencia puede apuntar a una cuenta
        # que se creó después que ella en el archivo).
        for a in data["accounts"]:
            acc = accounts_by_number.get(a["account_number"])
            if acc is None or acc.transactions:  # ya existía en memoria con su historial
                continue

            for t_data in a.get("transactions", []):
                destination = accounts_by_number.get(t_data["destination_account"]) if t_data["destination_account"] else None
                trans = Transaction(
                    type=t_data["type"], amount=t_data["amount"], origin_acc=acc,
                    destination_acc=destination, description=t_data["description"],
                    id=t_data["id"], date=datetime.fromisoformat(t_data["date"])
                )
                acc.transactions.append(trans)
                all_transactions_by_id[trans.id] = trans

            for c_data in a.get("cards", []):
                card = Card(
                    acc, c_data.get("pin", "0000"), c_data["is_credit_card"], c_data["is_debit_card"],
                    card_number=c_data["card_number"], cvv=c_data.get("cvv"),
                    expiration_date=datetime.fromisoformat(c_data["expiration_date"]),
                    is_blocked=c_data["is_blocked"]
                )
                acc.cards.append(card)

        self.global_transactions = list(all_transactions_by_id.values())

        # Logs 
        existing_log_ids = {log.id for log in self.logs}
        for log_data in data.get("logs", []):
            if log_data["id"] in existing_log_ids:
                continue
            employee = employees_by_dni.get(log_data["employee_dni"])
            if employee is None:
                continue  # el empleado ya no existe, se omite el log
            log = Log(
                employee, log_data["action"], log_data["status"], log_data["details"],
                id=log_data["id"], date=datetime.fromisoformat(log_data["date"])
            )
            self.logs.append(log)

        #  Auditoría 
        existing_audit_ids = {a.id for a in self.audit_history}
        for ah in data.get("audit_history", []):
            if ah.get("id") in existing_audit_ids:
                continue
            self.audit_history.append(AuditLog(
                ah["action_type"], ah["operator_name"], ah["target_name"], ah["target_dni"],
                details=ah.get("details", ""), timestamp=ah.get("timestamp"), id=ah.get("id")
            ))

        # Solicitudes de promoción / aumento salarial
        existing_promo_ids = {r.id for r in self.promotion_requests}
        for pr in data.get("promotion_requests", []):
            if pr.get("id") in existing_promo_ids:
                continue
            employee = employees_by_dni.get(pr["employee_dni"])
            if employee is not None:
                self.promotion_requests.append(PromotionRequest(employee, pr["reasons"], id=pr.get("id")))

        existing_salary_req_ids = {r.id for r in self.salary_requests}
        for sr in data.get("salary_requests", []):
            if sr.get("id") in existing_salary_req_ids:
                continue
            employee = employees_by_dni.get(sr["employee_dni"])
            if employee is not None:
                self.salary_requests.append(SalaryIncreaseRequest(employee, sr["reasons"], id=sr.get("id")))

        # Bono total acumulado 
        if "total_bonus" in data:
            self.bonus_admin.set_total_bonus(max(self.bonus_admin.get_total_bonus(), data["total_bonus"]))

        return True
        
