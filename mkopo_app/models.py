from django.db import models
from django.conf import settings

# Create your models here.
class InterestRate(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Interest rate as a decimal, e.g., 0.15 for 15%")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.rate * 100}%)"

class LoanDuration(models.Model):
    name = models.CharField(max_length=50, unique=True)
    months = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.months} months)"
    
    
class Loan(models.Model):
    LOAN_STATUS_CHOICES=(
        ('pending','pending'),
        ('approved','approved'),
        ('rejected','rejected'),
        ('disbursed','disbursed'),
        ('repaid','repaid'),
    )
    client=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='loans')
    guarantor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='guarantor_loans')
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    interest_rate=models.ForeignKey(InterestRate,on_delete=models.PROTECT)
    duration=models.ForeignKey(LoanDuration,on_delete=models.PROTECT)
    status=models.CharField(max_length=20,choices=LOAN_STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Loan for {self.client.username} by {self.guarantor.username}"
    

    
class LoanDocument(models.Model):
    DOCUMENT_TYPE_CHOICES=(
        ('national_id','National ID'),
        ('passport','Passport'),
        ('driver_license','Driver License'),
        ('bank_statement','Bank Statement'),
        ('weo_letter',"Ward Executive Officer Letter"),
        ('business_license','Business License'),
        ('tin certificate','TIN Certificate'),
        ('guarantor_letter','Guarantor Letter'),
        ('guarantor_national_id','Guarantor National ID'),
        ('guarantor_passport','Guarantor Passport'),
    )
    HOLDER_CHOICES=(
        ('client','Client'),
        ('guarantor','Guarantor'),
    )
    loan=models.ForeignKey(Loan,on_delete=models.CASCADE,related_name='documents')
    document=models.FileField(upload_to='loan_documents/')
    document_type=models.CharField(max_length=50,choices=DOCUMENT_TYPE_CHOICES,default='national_id')
    is_verified=models.BooleanField(default=False)
    holder=models.CharField(max_length=20,choices=HOLDER_CHOICES,default='client')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Document for {self.loan.client.username} by {self.loan.sponsor.username}"
    

    
    
    
    
    
    
  