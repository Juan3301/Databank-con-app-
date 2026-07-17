from datetime import datetime

class AuditLog:
    def __init__(self, action_type, operator_name, target_name, target_dni, details=""):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.action_type = action_type
        self.operator_name = operator_name
        self.target_name = target_name
        self.target_dni = target_dni
        self.details = details 

    def to_string(self):
        if self.action_type == "CREATE":
            return f"[{self.timestamp}] CREACIÓN: El operador {self.operator_name} creó al empleado {self.target_name} (DNI: {self.target_dni})."
        elif self.action_type == "DELETE":
            return f"[{self.timestamp}] DESPIDO: El operador {self.operator_name} eliminó al empleado {self.target_name} (DNI: {self.target_dni}). Motivo: {self.details}"