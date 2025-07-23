from mkopo_dto.mkopo_auth_dto import *
from .models import *
from graphql_jwt.decorators import login_required



class AuthQuery(graphene.ObjectType):
    get_userme=graphene.Field(UserObject)
    
    @staticmethod
    @login_required
    def resolve_userme(self,info):
        user=info.context.user
        return user