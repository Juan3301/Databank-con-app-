import uuid

class SalaryIncreaseRequest:
    def __init__(self, employee, reasons, id: str | None = None):
        self.id = id if id is not None else uuid.uuid4().hex[:8]
        self.employee = employee
        self.reasons = reasons
        
    def to_dict(self):
        return {
            "id": self.id,
            "employee_dni": self.employee.get_dni(),
            "reasons": self.reasons
        }