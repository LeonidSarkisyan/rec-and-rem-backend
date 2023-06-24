from typing import Optional

from pydantic import create_model


def make_optional(baseclass):
    # Extracts the fields and validators from the baseclass and make fields optional
    fields = baseclass.__fields__
    validators = {'__validators__': baseclass.__validators__}
    optional_fields = {key: (Optional[item.type_], None) for key, item in fields.items()}
    return create_model(f'{baseclass.__name__}Optional', **optional_fields, __validators__=validators)
