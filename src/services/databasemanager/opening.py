import short_url


class OpenManagerRepository:

    @classmethod
    async def create_open_url(cls, entity_id: int, n: int = 10):
        url = short_url.encode_url(entity_id, n)
        return url

    @classmethod
    async def get_entity_id(cls, entity_open_url):
        entity_id = short_url.decode_url(entity_open_url)
        return entity_id


class OpenManagerService(OpenManagerRepository):

    @classmethod
    async def get_open_url(cls, entity_open_url: str):
        try:
            entity_id = await super().get_entity_id(entity_open_url)
        except ValueError:
            raise NotValidCode
        else:
            return entity_id
