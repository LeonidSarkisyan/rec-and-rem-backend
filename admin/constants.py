from admin.config import RolesIDs

DEFAULT_ROLES = [
    {'id': RolesIDs.ADMIN_ID, 'name': 'admin', 'description': 'Can do everything'},
    {
        'id': RolesIDs.MODERATOR_ID,
        'name': 'moderator',
        'description': 'Can edit other people\'s records and regulate the activity of other users'
     },
    {'id': RolesIDs.USER_ID, 'name': 'user', 'description': 'Uses open functionality'},
]

DEFAULT_ROLES_IDS = [RolesIDs.ADMIN_ID, RolesIDs.MODERATOR_ID, RolesIDs.USER_ID]
