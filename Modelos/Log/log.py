import uuid
from Modelos.Roles.employee import Employee
from datetime import datetime

class Log:
    def __init__(self, employee: Employee, action: str, status: bool, details: str = "",
                 id: str | None = None, date: datetime | None = None):
        self.id = id if id is not None else uuid.uuid4().hex[:8]
        self.date = date if date is not None else datetime.now()
        self.employee = employee
        self.action = action
        self.status = status 
        self.details = details

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "employee_dni": self.employee.get_dni(),
            "action": self.action,
            "status": self.status,
            "details": self.details
        }
    
    def __str__(self) -> str:
         return (
            f"ID: {self.id} \n"
            f"Fecha: {self.date} \n"
            f"Empleado: {self.employee.name} \n"
            f"Acción: {self.action} \n"
            f"Estado: {self.status} \n"
            f"Detalles: {self.details} \n"
            )