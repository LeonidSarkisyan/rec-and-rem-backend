from src.exceptions.http import NotFound, AccessDenied, OwnEntity, NotValidCode, ErrorByCreating, PrivateResource


class Validator:

    @classmethod
    def is_exist(cls, entity, exception=NotFound):
        if not entity:
            raise exception

    @classmethod
    def is_open(cls, entity, exception=PrivateResource):
        if not entity.is_open:
            raise exception

    @classmethod
    def is_owner(cls, entity, user, exception=AccessDenied):
        if entity.user_id != user.id:
            raise exception
