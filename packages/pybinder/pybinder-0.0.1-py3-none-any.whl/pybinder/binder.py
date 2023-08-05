import json
from pybinder.field import BaseField
from pybinder.exceptions import Empty


class BinderMeta(type):
    def __new__(mcs, cls_name, bases, cls_dict):
        fields = {}
        attributes = {}
        alias_map = {}  # alias name to attribute name

        for name, attr in cls_dict.items():
            if isinstance(attr, BaseField):
                alias = name if attr.name is None else attr.name
                if alias in alias_map:
                    raise ValueError(f"Duplicate alias: '{alias}'")
                alias_map[alias] = name
                fields[name] = attr
            else:
                attributes[name] = attr

        attributes["fields"] = fields
        attributes["alias_map"] = alias_map
        return type.__new__(mcs, cls_name, bases, attributes)


class BaseBinder(metaclass=BinderMeta):

    def __setattr__(self, key, value):
        if key not in self.fields:
            raise AttributeError(f"Struct {self.__class__.__name__} has no attribute {key}")
        field = self.fields[key]
        if not isinstance(value, field.received_types()) and value is not Empty:
            raise TypeError(f"Unexpect type `{type(value).__name__}` for {field.__class__.__name__}")
        field.validate(value)

        super(BaseBinder, self).__setattr__(key, value)

    @classmethod
    def bind_json(cls, data):
        return cls.bind_dict(json.loads(data))

    @classmethod
    def bind_dict(cls, data):
        obj = cls()
        for field_alias, field_name in cls.alias_map.items():
            input_value = data.get(field_alias, Empty)
            field = cls.fields[field_name]
            value = field.cast_value(input_value)
            setattr(obj, field_name, value)

        return obj

    def dictify(self) -> dict:
        rv = {}
        for field_alias, field_name in self.alias_map.items():
            value = getattr(self, field_name, Empty)
            field = self.fields[field_name]

            if value is Empty:
                if field.omitempty:
                    continue
                else:
                    value = field.default()
            else:
                value = field.cast_field(value)
            rv[field_alias] = value
        return rv

    def jsonfy(self) -> str:
        return json.dumps(self.dictify())
