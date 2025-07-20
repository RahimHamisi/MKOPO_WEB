from mkopo_dto.mkopo_auth_dto import *
from .models import *
from graphql_jwt.decorators import login_required
from oauth2_provider.decorators import protected_resource


class AuthQuery(graphene.ObjectType):
    get_userme=graphene.Field(UserObject)
    
    @staticmethod
    @login_required
    @protected_resource(scopes=['read'])
    def resolve_userme(self,info):
        user=info.context.user
        return user