from src.services.copy_service import BaseCopyService
from src.abstract.dao import AbstractDaoService


class AbstractCopyService(BaseCopyService):
    dao = AbstractDaoService
