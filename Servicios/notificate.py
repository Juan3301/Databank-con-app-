from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Servicios.bank import Bank

class Notificate:
    def __init__(self, bank: "Bank"):
        self.bank = bank

    def send_notification(self, notification_type: str, message: str):
        notification_types = ["client", "employee"]
        message = f"Notificación: {message}"
        if notification_type not in notification_types:
            raise ValueError("Tipo de notificación inválida")
        elif notification_type == "client":
            print(f"Notificación enviada al cliente: {message}")
        elif notification_type == "employee":
            print(f"Notificación enviada al empleado: {message}")

  
    def notify_account_blocked(self):
          self.send_notification("client", "Su trajeta ha sido bloqueada.")