from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone



class CUSTOM_USER(AbstractUser):

    USER=[
        ('jobcreator','JOBCREATOR'),
        ('jobseeker','JOBSEEKER')
    ]
    usertype=models.CharField(choices=USER,null=True,max_length=100)

    def __str__(self):
        return f"{self.username}-{self.first_name}-{self.last_name}"
   


    

class JOOBModel(models.Model):

    job_type=[
        ('full-time','FULL-TIME'),
        ('part-time','PART-TIME'),
        ('contract','Contract'),
        ('internship','Internship'),
     
    ]

    user=models.ForeignKey(CUSTOM_USER,null=True,on_delete=models.CASCADE)

    description=models.TextField(max_length=10000, null=True)
    ememployment_type=models.CharField(choices= job_type,max_length=100, null=True)
    location=models.CharField(max_length=100, null=True)
    salary=models.CharField(max_length=100, null=True)
    company_namne=models.CharField(max_length=100, null=True)
    job_title=models.CharField(max_length=100, null=True)
    posted_date=models.DateField(auto_now_add=True)
    application_deadline=models.DateField(null=True,blank=True)
    img=models.ImageField(upload_to="media/img",null=True)

    

    def  __str__(self):
        return f"{self.user}"
    

class JOBAPPLYMODEL(models.Model):

    user=models.ForeignKey(CUSTOM_USER,null=True,on_delete=models.CASCADE)
    job=models.ForeignKey(JOOBModel,null=True,on_delete=models.CASCADE)

    resume=models.FileField(upload_to="media/resume",null=True)
    cover=models.TextField(max_length=100, null=True)
    salary=models.CharField(max_length=100, null=True)
    full_name=models.CharField(max_length=100, null=True)
    work_experience=models.CharField(max_length=100, null=True)
    skills=models.CharField(max_length=100, null=True)
    linkedin_url=models.URLField(max_length=100, null=True)
    expectted_salary=models.PositiveBigIntegerField(blank=True,null=True)

   


