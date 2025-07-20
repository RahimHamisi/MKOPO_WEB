import graphene



class UserObject(graphene.ObjectType):
    username=graphene.String()
    email=graphene.String()
    first_name=graphene.String()
    last_name=graphene.String()
    is_active=graphene.Boolean()
    is_staff=graphene.Boolean()
    is_admin=graphene.Boolean()
    


class UserInputObject(graphene.InputObjectType):
    username=graphene.String()
    email=graphene.String()
    password=graphene.String()
    first_name=graphene.String()
    last_name=graphene.String()
    role=graphene.String()