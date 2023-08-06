from .exc import ValidationError
from .expr import VarTree
from .planner import plan_granular


class _ExecutionContext:
    def __init__(self, session, modules, dependency_map=None, variables=None):
        self.session = session
        self.modules = modules
        self.dependency_map = dependency_map
        self.result = {}
        self.vartree = VarTree(variables or {})
        self._invalidates = {}

    def set_result(self, k, v):
        self.result[k] = v

    def set_var(self, k, v):
        self.vartree[k] = v

    def action_invalidated(self, action_name):
        return self._invalidates.get(action_name)

    def invalidate_dependencies(self, action_name):
        upstreams = self.dependency_map.get(action_name, [])
        for upstream in upstreams:
            if upstream not in self._invalidates:
                self._invalidates[upstream] = action_name


def validate_variables(request, variables):
    user_vars = set(variables)
    req_vars = request.required_variables

    missing = req_vars.difference(user_vars)
    if missing:
        raise ValidationError(
            message="missing variables",
            details=list(missing),
        )


def validate_modules(request, modules):
    user_mods = set(modules)
    req_operations = request.required_modules
    req_mods = set(e[0] for e in req_operations)

    missing = req_mods.difference(user_mods)
    if missing:
        raise ValidationError(
            message="unknown modules",
            details=list(missing),
        )

    unknown_operations = set()
    for mod, operation_name in req_operations:
        module = modules[mod]
        operation = module.get_operation(operation_name)
        if not operation:
            unknown_operations.add(f"{mod}.{operation_name}")

    if unknown_operations:
        raise ValidationError(
            message="unknown operations",
            details=list(unknown_operations),
        )



async def execute(request, session, modules, variables=None, explain=False):
    variables = variables or {}
    validate_variables(request, variables)
    validate_modules(request, modules)

    plan = plan_granular(request.actions)
    context = _ExecutionContext(
        session=session,
        modules=modules,
        variables=variables,
        dependency_map=build_dependency_map(plan.dependency_graph)
    )

    await plan.object_plan.run(context)

    out = {
        "result": context.result,
    }

    if explain:
        out["plan"] = plan.as_obj()

    return out


def build_dependency_map(dependency_graph):
    dm = {}
    for k, vs in dependency_graph.items():
        for v in vs:
            dm.setdefault(v, set()).add(k)
    return dm
