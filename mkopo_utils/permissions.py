# mkopo_utils/permissions.py
from functools import wraps
from graphql import GraphQLError

from mkopo_utils.mkopo_permissions_config import ROLE_PERMISSIONS


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(self, info, *args, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise GraphQLError("Authentication required")
            allowed_permissions = ROLE_PERMISSIONS.get(getattr(user, 'role', None), [])
            if permission not in allowed_permissions:
                raise GraphQLError("You do not have permission to perform this action")
            return func(self, info, *args, **kwargs)
        return wrapper
    return decorator