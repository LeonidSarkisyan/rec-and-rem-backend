
class Role:
    def __init__(self, name: str, role_id: int):
        self.name = name
        self.role_id = role_id

    def get_role_id(self) -> dict:
        return {"role_id": self.role_id}

    def is_this_role(self, role_id):
        return self.role_id == role_id

    def __repr__(self):
        return f'<Класс роли {self.name} id = {self.role_id}>'


class RolesSet:
    user = Role('user', 3)
    moderator = Role('moderator', 2)
    admin = Role('admin', 1)
