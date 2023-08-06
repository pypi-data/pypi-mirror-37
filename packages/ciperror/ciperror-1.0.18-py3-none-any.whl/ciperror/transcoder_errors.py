from ciperror import BaseCipError


class TranscoderServiceRequestError(BaseCipError):
    def __init__(self, message):
        super().__init__(
            code="TRE001",
            message="Erro no request para o Transcoder Service: {}".format(message),
            friendly_message="Erro no request para o Transcoder Service.",
            http_status=500)

