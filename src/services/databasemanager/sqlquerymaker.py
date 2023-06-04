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
                .where(search_attribute.ilike('%' + search_query + '%'))
        elif compare_attribute:
            query = select(model).where(compare_attribute == filter_value)
        else:
            query = select(model)

        return query


default_sql_query_maker = SQLQueryMaker()
