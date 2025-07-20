import graphene
from mkopo_auth.schema import AuthQuery
from mkopo_auth.views import AuthMutation

class Query(AuthQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)