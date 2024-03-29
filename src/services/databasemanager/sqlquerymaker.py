from sqlalchemy import select, update, delete, insert


class SQLQueryMaker:
    """ Создаёт гибкие sql-запросы по условию"""
    def select(
            self,
            model,
            search_field: str,
            compare_attribute=None,
            filter_value: int = None,
            search_query: str = None
    ):
        if search_query:
            search_attribute = getattr(model, search_field)

            query = select(model) \
                .where(compare_attribute == filter_value) \
                .where(search_attribute.ilike('%' + search_query + '%')).order_by(model.id.desc())
        elif compare_attribute:
            query = select(model).where(compare_attribute == filter_value).order_by(model.id.desc())
        else:
            query = select(model).order_by(model.id.desc())

        return query


default_sql_query_maker = SQLQueryMaker()


class BaseSQLMaker:
    model = None

    @classmethod
    def select(cls, entity_id: int):
        query = select(cls.model).where(cls.model.id == entity_id)
        return query

    @classmethod
    def insert(cls, data_dict: dict, returning):
        stmt = insert(cls.model).returning(returning).values(**data_dict)
        return stmt
