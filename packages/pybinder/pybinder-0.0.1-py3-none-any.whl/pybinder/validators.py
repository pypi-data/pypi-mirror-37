from pybinder.exceptions import ValidateError, Empty


class BaseValidator:
    def __init__(self):
        pass

    def __call__(self, value):
        raise NotImplementedError


class NotEmpty(BaseValidator):
    def __call__(self, value):
        if value is Empty:
            raise ValidateError("Field except value")  # TODO: info
