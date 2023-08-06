import re
from collections import UserDict

from .exc import VarAlreadyDefinedError, VarNotFountError


class Requirement:
    def __init__(self, module, name):
        self.module = module
        self.name = name

    @property
    def is_global(self):
        return self.module is None

    @property
    def full_name(self):
        if self.module:
            return self.module + "." + self.name
        return self.name


class Expression:
    def __init__(self, captures):
        self.captures = captures

    def resolve(self, vartree):
        items = [c.resolve(vartree) for c in self.captures]
        if len(items) == 1:
            return items[0]
        return "".join((str(el) for el in items))

    def requires(self):
        r = (c.requires() for c in self.captures)
        r = (c for c in r if c is not None)
        return set(r)

    def __str__(self):
        return ", ".join(map(str, self.captures))


class VarTree(UserDict):  # pylint: disable=too-many-ancestors
    def __setitem__(self, key, value):
        if key in self:
            raise VarAlreadyDefinedError(
                message="variable already defined",
                details={"key": key},
            )
        super().__setitem__(key, value)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            raise VarNotFountError(
                message="variable not found",
                details={"key": key}
            )


class Capture:
    def __init__(self, value, static=True):
        self.value = value

    def __str__(self):
        return "Capture({})".format(self.value)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def requires(self):
        return None


class StaticCapture(Capture):
    def resolve(self, _vartree):
        return self.value

    def __str__(self):
        return "StaticCapture({})".format(self.value)


class DynamicCapture(Capture):
    def resolve(self, vartree):
        return vartree[self.value]

    def __str__(self):
        return "DynamicCapture({})".format(self.value)

    def requires(self):
        elements = self.value.split(".", 1)
        if len(elements) == 2:
            return Requirement(module=elements[0], name=elements[1])
        return Requirement(module=None, name=elements[0])


PARAMETER_PATTERN = re.compile(r'(\${([^}]+?)})')


def split(expr):
    found_dynamic = False
    if not isinstance(expr, str):
        return [StaticCapture(expr)], found_dynamic
    start = 0
    end = len(expr)
    out = []
    for el in PARAMETER_PATTERN.finditer(expr):
        ns, ne = el.span()
        if ns > start:
            out.append(StaticCapture(value=expr[start:ns]))
        out.append(DynamicCapture(value=el.group(2)))
        found_dynamic = True
        start = ne

    if start != end:
        out.append(StaticCapture(value=expr[start:end]))
    return out, found_dynamic
