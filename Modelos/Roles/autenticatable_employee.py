from datetime import datetime
from Modelos.Roles.employee import Employee
from Modelos.AutenticableHelper.autenticatable_helper import AutenticatableHelper

class AutenticatableEmployee(Employee):
    def __init__(self, name: str, dni: int, position: str, salary: float, experience: int, password: str):
        super().__init__(name, dni, position, salary, experience)
        self._helper = AutenticatableHelper()
        self.__password = password
        self.locked_until = None
        self.register_date = datetime.now()

    def get_password(self):
        return self.__password
    
    def authenticate_user(self, new_password: str):
        return self._helper.comparate_passwords(self.get_password(), new_password)

    def obtain_bonus(self) -> float:
        return 0
    
    def is_blocked(self):
        if self.locked_until is not None and datetime.now() >= self.locked_until:
            self.locked_until = None
            return False
        return self.locked_until is not None
    
    def to_dict(self):
        data = super().to_dict()
        data["password"] = self.get_password()
        data["register_date"] = self.register_date.isoformat()
        return data