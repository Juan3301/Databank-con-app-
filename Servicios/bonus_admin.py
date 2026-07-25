from Modelos.Roles.employee import Employee
class BonusAdmin:
    def __init__(self) -> None:
        self.__total_bonus: float = 0.0

    def register(self, employee: Employee):
        self.__total_bonus += employee.obtain_bonus()

    def get_total_bonus(self):
        return self.__total_bonus

    def set_total_bonus(self, value: float):
        self.__total_bonus = value
        