from ciperror import BaseCipError


class FileCopyServiceRequestError(BaseCipError):
    def __init__(self, message):
        super().__init__(
            code="FLC001",
            message="Erro no request para o File Copy Service: {}".format(message),
            friendly_message="Erro no request para o File Copy Service.",
            http_status=500)