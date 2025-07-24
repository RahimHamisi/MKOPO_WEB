from .models import *
import graphene
import graphql_jwt
from django.contrib.auth import authenticate
from mkopo_dto.mkopo_auth_dto import *
from mkopo_dto.mkopo_response import ResponseObjects

# Create your views here.
class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input = UserInputObject(required=True)

    output = graphene.Field(UserResponseObject)

    @classmethod
    def mutate(cls, root, info, input):
        if CustomUser.objects.filter(username=input.username).exists():  
            response=ResponseObjects.get_response(id=8)
            output=UserResponseObject(user=None,response=response)
            return CreateUserMutation(output=output)
        if CustomUser.objects.filter(email=input.email).exists():
            response=ResponseObjects.get_response(id=9)
            output=UserResponseObject(user=None,response=response)
            return CreateUserMutation(output=output)
        if input.role != 'client':
            response=ResponseObjects.get_response(id=12)
            output=UserResponseObject(user=None,response=response)
            return CreateUserMutation(output=output)
        user = CustomUser(
            username=input.username,
            email=input.email,
            first_name=input.first_name,
            last_name=input.last_name,
            role=input.role
        )
        print(user)
        user.set_password(input.password)
        user.save()
        print(user)
        response=ResponseObjects.get_response(id=5)
        print(response)
        output=UserResponseObject(user=user, response=response)
        print(output)
        return CreateUserMutation(output=output)

class LoginUserMutation(graphene.Mutation):
    class Arguments:
        input = LoginInputObject(required=True)

    output = graphene.Field(LoginResponseObject)

    @classmethod
    def mutate(cls, root, info, input):
        user = authenticate(username=input.username, password=input.password)
        print(user)
        if user is None:
            response=ResponseObjects.get_response(id=2)
            output=LoginResponseObject(response=response)
            return LoginUserMutation(output=output)
        access_token = graphql_jwt.shortcuts.get_token(user)
        refresh_token=graphql_jwt.shortcuts.create_refresh_token(user)
        response=ResponseObjects.get_response(id=1)
        output=LoginResponseObject(user=user, access_token=access_token, refresh_token=refresh_token, response=response)
        return LoginUserMutation(output=output)

class UpdateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        role = graphene.String()

    user = graphene.Field(UserObject)

    @classmethod
    def mutate(cls, root, info, username=None, email=None, role=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        if username:
            user.username = username
        if email:
            user.email = email
        if role:
            if user.role != 'admin':
                raise Exception("Only admin can change roles.")
            user.role = role
        user.save()
        return UpdateUser(user=user)

class AuthMutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    login_user = LoginUserMutation.Field()
    update_user = UpdateUser.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    