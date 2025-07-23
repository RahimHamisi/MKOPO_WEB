import graphene
from mkopo_dto.mkopo_response import ResponseObjects


class UserObject(graphene.ObjectType):
    username=graphene.String()
    email=graphene.String()
    first_name=graphene.String()
    last_name=graphene.String()
    is_active=graphene.Boolean()
    is_staff=graphene.Boolean()
    is_admin=graphene.Boolean()
    role=graphene.String()
class UserResponseObject(graphene.ObjectType):
    user=graphene.Field(UserObject)
    response=graphene.Field(ResponseObjects)
    


class UserInputObject(graphene.InputObjectType):
    username=graphene.String()
    email=graphene.String()
    password=graphene.String()
    first_name=graphene.String()
    last_name=graphene.String()
    role=graphene.String()

class LoginInputObject(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)

class LoginOutputObject(graphene.ObjectType):
    user = graphene.Field(UserObject)
    accessoken = graphene.String()
    refresh_token = graphene.String()
    
    
class LoginResponseObject(graphene.ObjectType):
    user = graphene.Field(UserObject)
    access_token = graphene.String()
    refresh_token = graphene.String()
    response = graphene.Field(ResponseObjects)