

class BaseSQLExecutor:

    @classmethod
    def execute(cls, query):
        try:
            result = await session.execute(query)
        except DBAPIError:
            raise NotValidCode
        else:
            return result


class SQLExecutorService(BaseSQLExecutor):
    async def valid_code(self, func):
        try:
            result = await func()
        except DBAPIError:
            raise NotValidCode
        else:
            return result
