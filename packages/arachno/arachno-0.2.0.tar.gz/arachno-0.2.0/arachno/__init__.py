
from .request import Request, Action, Options, Duration
from .executor import execute

class BaseModule:
    async def dispatch(self, operation_name, session, **kwargs):
        operation = self.get_operation(operation_name)
        kwargs = self.prepare_arguments(operation_name, **kwargs)
        return await operation(session, **kwargs)

    def prepare_arguments(self, operation_name, **kwargs):
        return kwargs

    def get_operation(self, operation_name):
        return getattr(self, operation_name, None)
