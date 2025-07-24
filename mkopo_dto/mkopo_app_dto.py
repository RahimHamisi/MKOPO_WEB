import graphene

from mkopo_app.models import Loan
from mkopo_dto.mkopo_response import ResponseObjects
from mkopo_dto.mkopo_auth_dto import UserObject



class LoanDocumentInput(graphene.InputObjectType):
    document=graphene.String(required=True)
    document_type=graphene.String(required=True)
    is_verified=graphene.Boolean(default=False)
    holder=graphene.String(required=True)
    
class LoanApplicationInput(graphene.InputObjectType):
    amount=graphene.Float(required=True)
    duration=graphene.INT()
    guarantor_id=graphene.ID(required=True)
    documents=graphene.List(LoanDocumentInput)
    

    
class InterestRateObject(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    rate = graphene.Float()

class LoanDurationObject(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    months = graphene.Int()

class LoanObject(graphene.ObjectType):
    loan_id = graphene.ID()
    client = graphene.Field(UserObject)
    guarantor = graphene.Field(UserObject)
    amount = graphene.Float()
    interest_rate = graphene.Field(InterestRateObject)
    duration = graphene.Field(LoanDurationObject)
    status = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    
    def resolve_loan_id(self,info):
        return self.id
    
    def resolve_client(self,info):
        return UserObject(id=self.client.id,username=self.client.username,email=self.client.email)
    
    def resolve_guarantor(self,info):
        return UserObject(id=self.guarantor.id,username=self.guarantor.username,email=self.guarantor.email)
    
    
class LoanApplicationOutput(graphene.ObjectType):
    loan=graphene.Field(LoanObject)
    response=graphene.Field(ResponseObjects) 

    
    
    