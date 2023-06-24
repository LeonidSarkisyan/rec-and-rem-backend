from typing import Optional

from pydantic import BaseModel, create_model


class Login(BaseModel):
    email: str
    password: str


class RoleBase(BaseModel):
    name: str
    description: str


class RoleCreate(RoleBase):
    pass


def make_optional(baseclass):
    fields = baseclass.__fields__
    validators = {'__validators__': baseclass.__validators__}
    optional_fields = {key: (Optional[item.type_], None) for key, item in fields.items()}
    return create_model(f'{baseclass.__name__}Optional', **optional_fields, __validators__=validators)


RoleUpdate = make_optional(RoleBase)
