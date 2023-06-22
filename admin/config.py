import os

from dotenv import load_dotenv

load_dotenv()


class AdminInfo:
    ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
    ADMIN_PASS = str(os.environ.get('ADMIN_PASS'))
    ID = int(os.environ.get('ADMIN_ID'))


class RolesIDs:
    ADMIN_ID = int(os.environ.get('ADMIN_ID'))
    MODERATOR_ID = int(os.environ.get('MODERATOR_ID'))
    USER_ID = int(os.environ.get('USER_ID'))
