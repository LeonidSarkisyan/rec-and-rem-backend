import sqlalchemy as sa

from src.database import Base


def duplicate_object(old_obj):
    # SQLAlchemy related data class?
    if not isinstance(old_obj, Base):
        raise TypeError('The given parameter with type {} is not '
                        'mapped by SQLAlchemy.'.format(type(old_obj)))

    mapper = sa.inspect(type(old_obj))
    new_obj = type(old_obj)()

    for name, col in mapper.columns.items():
        # no PrimaryKey not Unique
        if not col.primary_key and not col.unique:
            setattr(new_obj, name, getattr(old_obj, name))

    return new_obj
