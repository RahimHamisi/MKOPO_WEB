from .models import *
import graphene
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate, login
from oauth2_provider.decorators import protected_resource
from mkopo_dto.mkopo_auth_dto import *

# Create your views here.
class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input=UserInputObject()
        
        
    output=graphene.Field(UserObject)
    @classmethod
    def mutate(self,root, info, input):
        if CustomUser.objects.filter(username=input.username).exists():
            raise Exception("Username already exists")
        if CustomUser.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")
        user = CustomUser(username=input.username, role=input.role)
        user.set_password(input.password)
        user.save()
        return CreateUserMutation(output=user)

class LoginMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username, password):
        user = authenticate(request=info.context, username=username, password=password)
        if user:
            login(request=info.context, user=user)
            return LoginMutation(success=True, message="Logged in successfully")
        return LoginMutation(success=False, message="Invalid credentials")


class UpdateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        role = graphene.String()

    user = graphene.Field(UserObject)

    @protected_resource(scopes=['write'])
    def mutate(self, info, username=None, email=None, role=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        if username:
            user.username = username
        if email:
            user.email = email
        if role:
            user.role = role
        user.save()
        return UpdateUser(user=user)

class AuthMutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    login_user=LoginMutation.Field()
    update_user=UpdateUser.Field()
    