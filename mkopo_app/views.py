from django.shortcuts import render
import graphene

# Create your views here.
from mkopo_dto.mkopo_app_dto import LoanApplicationInput, LoanApplicationOutput
from mkopo_dto.mkopo_response import ResponseObjects
from mkopo_dto_builder.mkopo_dto_builder import LoanApplicationBuilder
from mkopo_utils.permissions import permission_required


class ApplyForLoanMutation(graphene.Mutation):
    class Arguments:
        input=LoanApplicationInput(required=True)
        
    output=graphene.Field(LoanApplicationOutput)
    
    @classmethod
    @permission_required('create_loan')
    def mutate(cls,root,info,input):
        user=info.context.user
        loan=LoanApplicationBuilder.apply_for_loan(user,input)
        response=ResponseObjects.get_response(id=13)
        output=LoanApplicationOutput(loan=loan,response=response)
        return ApplyForLoanMutation(output=output)
    
    
class Mutation(graphene.ObjectType):
    apply_for_loan=ApplyForLoanMutation.Field()
    
    
    
    
