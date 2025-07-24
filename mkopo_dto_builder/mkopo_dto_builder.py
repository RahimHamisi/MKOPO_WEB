import base64
from mkopo_auth.models import *
from mkopo_app.models import *
from django.core.files.base import ContentFile

class LoanApplicationBuilder:
    
  
    
    @staticmethod
    def validate_user_profile(user):
        if user.gender not in ['male', 'female']:
            raise Exception("Gender must be specified as 'male' or 'female'.")
        if not user.phone_number or not user.address:
            raise Exception("Phone number and address are required.")
    
    @staticmethod
    def get_related_object(duration_id,interest_rate_id,guarantor_id):
        try:
            duration = LoanDuration.objects.get(id=duration_id, is_active=True)
            interest_rate = InterestRate.objects.get(id=interest_rate_id, is_active=True)
            guarantor = CustomUser.objects.get(id=guarantor_id)
        except (LoanDuration.DoesNotExist, InterestRate.DoesNotExist, CustomUser.DoesNotExist):
            raise Exception("Invalid duration, interest rate, or guarantor.")
        return duration, interest_rate, guarantor
    
    @staticmethod
    def validate_required_documents(documents,requirements):
        for holder, doc_types in requirements:
            for doc_type in doc_types:
                if not any(doc.doc_type == doc_type and doc.holder == holder for doc in documents):
                    raise Exception(f"{holder.title()} must provide {doc_type.replace('_', ' ').title()}.")
    
    
    @staticmethod
    def handle_file_upload(doc,user_id):
        if doc.file.startswith('data:'):
            format,imgstr =doc.file.split(';base64,')
            ext=format.split('/')[-1]
            file_name = f"{doc.doc_type}_{doc.holder}_{user_id}.{ext}"
            return ContentFile(base64.b64decode(imgstr),name=file_name)
        else:
            return ContentFile(doc.file,name=doc.file.name)
   
    @staticmethod
    def apply_for_loan(user, input):
        LoanApplicationBuilder.validate_user_profile(user)
        duration, interest_rate, guarantor = LoanApplicationBuilder.get_related_objects(
            input.duration_id, input.interest_rate_id, input.guarantor_id
        )
        LoanApplicationBuilder.validate_required_documents(input.documents, [
            ('client', ['national_id', 'passport', 'weo_letter']),
            ('guarantor', ['guarantor_national_id', 'guarantor_letter'])
        ])
        if Loan.objects.filter(client=user, status='pending').exists():
            raise Exception("You already have a pending loan application.")

        loan = Loan.objects.create(
            client=user,
            guarantor=guarantor,
            amount=input.amount,
            duration=duration,
            interest_rate=interest_rate,
            status='pending'
        )
        for doc in input.documents:
            file = LoanApplicationBuilder.handle_file_upload(doc, user.id)
            LoanDocument.objects.create(
                loan=loan,
                document=file,
                document_type=doc.doc_type,
                holder=doc.holder
            )
        return loan