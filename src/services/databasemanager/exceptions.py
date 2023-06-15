class DataBaseManagerException(Exception):
    pass


class NotUseParentModel(DataBaseManagerException):
    pass


class DoNotSetModel(DataBaseManagerException):
    pass
