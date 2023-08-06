

class ArachnoError(Exception):
    def __init__(self, message, details):
        super().__init__(message)
        self.message = message
        self.details = details

    def as_obj(self):
        return {
            "message": self.message,
            "details": self.details,
        }


class ValidationError(ArachnoError):
    def __str__(self):
        return ";".join(["{} {}".format(k, v) for k, v in self.details.items()])


class VarNotFountError(ArachnoError):
    pass


class VarAlreadyDefinedError(ArachnoError):
    pass


class ConfigurationError(ArachnoError):
    pass
