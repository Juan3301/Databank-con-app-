from Modelos.AutenticableHelper.autenticatable_helper import AutenticatableHelper
class CommercialPartner:
    def __init__(self) -> None:
        self._helper = AutenticatableHelper()
        self.clave: str | None = None

    def autenticar_usuario(self, clave: str) -> bool:
        return self._helper.comparate_passwords(self.clave, clave)
    
    def to_dict(self):
        return {
            "clave": self.clave
        }