from datetime import datetime
class Client:
    def __init__(self, name: str, dni: int, age: int, profession: str):
        self.name = name
        self.dni = dni
        self.age = age
        self.profession = profession
        self.credits = []
        self.is_blacklisted = False
        self.blacklist_reason = ""
        self.registration_date: datetime | None = None

    def add_credit(self, credit):
        self.credits.append(credit)

    def __str__(self) -> str:
        return f"Cliente: {self.name}, Dni: {self.age}"

    def to_dict(self):
        return {
            "name": self.name,
            "dni": self.dni,
            "age": self.age,
            "profession": self.profession,
            "is_blacklisted": self.is_blacklisted,
            "blacklist_reason": self.blacklist_reason,
            "credits": [credit.to_dict() for credit in self.credits]
        }