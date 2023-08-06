import asyncio
import time
from copy import copy
from datetime import timedelta
from typing import Any, Dict

import attr.validators as attrv
from attr import attrib, attrs
from cached_property import cached_property
from typing_extensions import Protocol

from .duration import from_str as duration_from_str
from .exc import ConfigurationError, ValidationError
from .expr import Expression
from .expr import split as split_expression
from .internal import assert_fields, recur


class Resolver(Protocol):
    def resolve(self, definition: Any) -> Any:
        pass


@attrs
class Duration:
    label = attrib(validator=attrv.instance_of(str))
    value = attrib(validator=attrv.optional(attrv.instance_of(timedelta)))

    @classmethod
    def from_str(cls, label):
        if not label:
            return cls(label="none", value=None)
        return cls(
            label=label,
            value=duration_from_str(label)
        )

    def seconds(self):
        if self.value is None:
            return None
        return self.value.total_seconds()  # pylint: disable=no-member


@attrs
class Options:
    timeout = attrib(validator=attrv.instance_of(Duration), convert=Duration.from_str, default="")
    suppress = attrib(validator=attrv.instance_of(bool), default=False)

    @classmethod
    def from_obj(cls, obj):
        assert_fields(cls, obj)
        return cls(**obj)


@attrs
class Request:
    actions: Dict[str, "Action"] = attrib(validator=attrv.instance_of(dict))

    def __attrs_post_init__(self):
        self._validate()

    @classmethod
    def from_obj(cls, obj):
        assert_fields(cls, obj)
        obj["actions"] = {
            n: Action.from_obj(a, name=n)
            for n, a in obj["actions"].items()
        }
        return cls(**obj)

    @property
    def required_modules(self):
        return copy(self._required_modules)

    @property
    def required_variables(self):
        return copy(self._required_variables)

    @cached_property
    def _required_variables(self):
        """Returns variables needed to execute this request"""

        out = set()
        for action in self.actions.values():  # pylint: disable=no-member
            requirements = action.requires()
            for requirement in requirements:
                if requirement.is_global:
                    out.add(requirement.full_name)
        return out

    @cached_property
    def _required_modules(self):
        out = set()
        for action in self.actions.values():  # pylint: disable=no-member
            out.add((action.module, action.operation))
        return out

    def _validate(self):
        self._validate_dependencies()

    def _validate_dependencies(self):
        definitions = self.required_variables
        args = set()
        requesters = {}

        for action_name, action in self.actions.items():  # pylint: disable=no-member
            for definition in action.defines:
                global_key = action_name + "." + definition
                definitions.add(global_key)

            requirements = action.requires()
            for requirement in requirements:
                full_name = requirement.full_name
                if requirement.module == action_name:
                    raise ValidationError(
                        message="reference to self-defined arg",
                        details={"arg": full_name}
                    )

                requesters.setdefault(full_name, []).append(action_name)
                args.add(full_name)

        not_defined = args.difference(definitions)
        if not_defined:
            tmpl = "required by {} but not defined"
            errs = {k: tmpl.format(
                ",".join(requesters[k])) for k in not_defined}
            raise ValidationError(
                message="undefined arguments",
                details=errs
            )


@attrs
class Action:
    module = attrib(validator=attrv.instance_of(str))
    operation = attrib(validator=attrv.instance_of(str))
    args = attrib(validator=attrv.instance_of(dict), factory=dict)
    defines = attrib(validator=attrv.instance_of(dict), factory=dict)
    options = attrib(validator=attrv.instance_of(Options), factory=Options)
    name = attrib(validator=attrv.optional(attrv.instance_of(str)), default=None)

    @classmethod
    def from_obj(cls, obj, name=None):
        assert_fields(cls, obj)
        obj["module"], obj["operation"] = _parse_operation(obj)
        obj["args"] = wrap_arguments(obj.get("args", {}))
        if name is not None:
            obj["name"] = name
        if obj.get("options"):
            obj["options"] = Options.from_obj(obj["options"])
        return cls(**obj)

    def requires(self):
        out = []

        def _collect(node):
            if isinstance(node, Expression):
                out.extend(node.requires())
        recur(_collect, self.args)
        return set(out)

    async def _run(self, context, loop=None):
        args = substitute_args(self.args, context.vartree)
        module = context.modules[self.module]
        coro = module.dispatch(self.operation, context.session, **args)
        start = time.monotonic()
        result = await asyncio.wait_for(coro, timeout=self.options.timeout.seconds(), loop=loop)  # pylint: disable=no-member
        return result, time.monotonic() - start

    async def run(self, context, loop=None):
        reason = context.action_invalidated(self.name)
        if reason is not None:
            return Output(
                failed=True,
                failure_details={
                    "type": "invalidated",
                    "value": reason,
                },
            )

        try:
            result, took = await self._run(context, loop=loop)
        except asyncio.TimeoutError:
            return Output(
                failed=True,
                failure_details={
                    "type": "timeout",
                    "value": self.options.timeout.label,  # pylint: disable=no-member
                },
            )

        if result.failed:
            return Output(
                failed=True,
                took=took,
                failure_details={
                    "type": "module_error",
                    "value": result.json,
                },
            )

        return Output(
            variables=self._resolve_defines(result) if not result.failed else {},
            failed=False,
            data=result.json if not self.options.suppress else None,  # pylint: disable=no-member
            took=took,
        )

    def _resolve_defines(self, resolver: Resolver) -> Dict[str, Any]:
        return {
            "{}.{}".format(self.name, key): resolver.resolve(definition)
            for key, definition in self.defines.items()  # pylint: disable=no-member
        }


@attrs
class Output:
    failed = attrib(validator=attrv.instance_of(bool))
    failure_details = attrib(validator=attrv.instance_of(dict), factory=dict)
    variables = attrib(validator=attrv.instance_of(dict), factory=dict)
    data = attrib(factory=dict)
    took = attrib(default=None)


def _parse_operation(obj):
    module = obj.get("module")
    operation = obj.get("operation")

    if module and operation:
        return module, operation

    if operation and "." in operation:
        return operation.split(".", 1)

    raise ConfigurationError(
        message="invalid operation",
        details={
            "module": module,
            "operation": operation
        })


def wrap_arguments(args):
    return recur(_wrap_expression, args)


def _wrap_expression(value):
    if not isinstance(value, str):
        return value

    expr, is_dynamic = split_expression(value)
    if is_dynamic:
        return Expression(expr)
    return value


def substitute_args(args, vartree):
    def _resolve(node, vartree=None):
        if isinstance(node, Expression):
            return node.resolve(vartree)
        return node
    return recur(_resolve, args, vartree=vartree)
