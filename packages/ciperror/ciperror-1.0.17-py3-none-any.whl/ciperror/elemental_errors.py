from ciperror import BaseCipError


class ElementalServiceRequestError(BaseCipError):
    def __init__(self, message):
        super().__init__(
            code="ELE001",
            message="Erro no request para o Elemental Service: {}".format(message),
            friendly_message="Erro no request para o Elemental Service.",
            http_status=500)

