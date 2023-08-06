from attr import fields_dict
from .exc import ConfigurationError


def assert_fields(cls, obj: dict) -> None:
    cls_fields = fields_dict(cls)
    requested_fields = set(obj)
    diff = requested_fields.difference(cls_fields)
    if diff:
        raise ConfigurationError(
            message="unknown fields",
            details=list(diff),
        )


def recur(callback, node, **kwargs):
    if isinstance(node, (tuple, list)):
        new_node = [recur(callback, el, **kwargs) for el in node]
    elif isinstance(node, dict):
        new_node = {k: recur(callback, v, **kwargs) for k, v in node.items()}
    else:
        new_node = callback(node, **kwargs)
    return new_node
