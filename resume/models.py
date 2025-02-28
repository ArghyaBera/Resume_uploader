from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Res(models.Model):
    # user=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)

    name=models.CharField(max_length=100)
    gen_choice={ 'M' :'Male', 'F':'female'}
    gender=models.CharField(choices=gen_choice,max_length=1)
    dob=models.DateField(auto_now=False, auto_now_add=False)
    loc=models.CharField(max_length=100)
    mob=models.IntegerField()
    pdf=models.FileField(upload_to='files')



