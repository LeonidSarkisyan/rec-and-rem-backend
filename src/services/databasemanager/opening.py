import short_url


class OpenManager:

    @staticmethod
    async def create_open_url(entity_id: int, n: int = 10):
        url = short_url.encode_url(entity_id, n)
        return url

    @staticmethod
    async def get_entity_id(entity_open_url):
        entity_id = short_url.decode_url(entity_open_url)
        return entity_id
