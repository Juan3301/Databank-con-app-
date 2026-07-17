class Employee:
    total_employees: int = 0
    
    def __init__(self, name: str, dni: int, position: str, salary: float, experience: int) -> None:
        Employee.total_employees +=1
        self.name = name
        self.__position = position
        self.__dni = dni
        self.__salary = salary
        self.experience = experience
        self.is_blocked = False
        self.failed_attempts = 0
        self.can_change_role = False
        self.locked_until = None

    def get_position(self):
        return (self.__position)
    
    def set_position(self, new_position):
        self.__position = new_position

    def get_dni(self):
        return (self.__dni)
    
    def get_salary(self):
        return (self.__salary)
    
    def set_salary(self, new_salary):
        self.__salary = new_salary
    
    def obtain_bonus(self) -> float:
        raise NotImplementedError("El método debe ser implementado en la sublclase.")

    def raise_salary(self):
        self.set_salary(
            self.get_salary() * (1 + self.percentage_increase())
        )
    
    def can_approve_credit(self, amount: float)-> bool:
        return False
    
    def can_modify_salary(self, employee: "Employee", amount: float)-> bool:
        return False
    
    def can_see_reports(self) ->bool:
        return False
    
    def can_see_information(self) -> bool:
        return False
    
    def can_approve_transfer(self, amount: float) -> bool:
        return False
    
    def can_create_user(self) -> bool:
        return False
    
    def can_delete_user(self) ->bool:
        return False
    
    def can_raise_salary(self, employee: "Employee") -> bool:
        return False
    
    def percentage_increase(self) -> float:
        return 0.01
    
    def can_request_promotion(self):
        return self.experience >= 5
    
    def to_dict(self):
        return {
            "employee_type": type(self).__name__,
            "name": self.name,
            "dni": self.get_dni(),
            "position": self.get_position(),
            "salary": self.get_salary(),
            "experience": self.experience,
            "is_blocked": self.is_blocked,
            "failed_attempts": self.failed_attempts,
            "can_change_role": self.can_change_role,
            "locked_until": self.locked_until.isoformat() if self.locked_until else None
        }
    
    def __str__(self):
        return(
            f"Nombre: {self.name}\n"
            f"Dni: {self.get_dni()}\n"
            f"Experiencia: {self.experience}\n"
        )