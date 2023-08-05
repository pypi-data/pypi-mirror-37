from pybinder.exceptions import Empty


class BaseField:
    def __init__(self, alias=None, omitempty=True, validators=()):
        if isinstance(alias, str) and not len(alias):
            raise ValueError("alias except a non-empty string")
        self.name = alias
        self.omitempty = omitempty
        self.validators = validators

    def validate(self, value):
        for validator in self.validators:
            validator(value)

    def default(self):
        raise NotImplementedError

    def cast_value(self, raw_value):
        # convert input value to struct attribute
        return raw_value

    def cast_field(self, field_value):
        # convert struct attribute to output value
        return field_value

    def received_types(self):
        raise NotImplementedError


class NumberField(BaseField):
    def default(self):
        return int()

    def received_types(self):
        return int, float


class StringField(BaseField):
    def default(self):
        return str()

    def received_types(self):
        return str


class BoolField(BaseField):
    def default(self):
        return bool()

    def received_types(self):
        return bool


class ArrayField(BaseField):
    def default(self):
        return list()

    def received_types(self):
        return list, tuple, set


class DictField(BaseField):
    def default(self):
        return dict()

    def received_types(self):
        return dict


class StructField(BaseField):
    def __init__(self, struct, *args, **kwargs):
        self.struct = struct
        super(StructField, self).__init__(*args, **kwargs)

    def default(self):
        return None

    def cast_value(self, raw_value):
        if raw_value is None or raw_value is Empty:
            return raw_value
        return self.struct.bind_dict(raw_value)

    def cast_field(self, field_value):
        if field_value is None:
            return field_value
        return field_value.dictify()

    def received_types(self):
        return dict
