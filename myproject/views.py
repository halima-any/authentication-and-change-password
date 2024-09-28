from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import IntegrityError
from myapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash




def base(req):
    return render(req,"base.html")


@login_required
def home(req):


    return render(req,"home.html")


def loginPage(req):
    if req.method == 'POST':
        username=req.POST.get('username')
        password=req.POST.get('password')

        if not username or not password:
            messages.warning(req,"Both username and password are required")
            return render(req, "loginPage.html")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(req, user)
            messages.success(req,'Login Successfully!')
            return redirect("home")
        else:
            messages.warning(req,"Invalid username or password")

    return render(req, "loginPage.html")

def register(req):
    if req.method == 'POST':
        username=req.POST.get('username')
        usertype=req.POST.get('usertype')
        password=req.POST.get('password')
        confirm_password=req.POST.get('confirm_password')
        if not all([username,usertype,password,confirm_password]):
            messages.warning(req,"All fields are requierd.")
                
            return render(req,'register.html')

        if password != confirm_password:
            messages.warning(req,"password do not matched.")   
            return render(req,'register.html')

          
        if len (password)<8:
            messages.warning(req,"password must be at least 8  character .")  
            return render(req,'register.html')
        

        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(req, "Password must contain both letters and numbers")
            return render(req,'register.html')
           
        try:
            user = CUSTOM_USER.objects.create_user(
                username=username,
                usertype=usertype,
                password=password
            )
            messages.success(req, "Account created successfully! Please log in.")
            return redirect("loginPage")
        except IntegrityError:
            messages.warning(req, "Username or email already exists")
            return render(req,"register.html")

    return render(req,"register.html")



def logoutPage(req):
    logout(req)
    messages.success(req,"you have logged out successfully")
    return redirect('loginPage')

@login_required
def joobfeed(req):

    data=JOOBModel.objects.all()

    text={
        "data":data
    }

    return render (req,'joobfeed.html',text)

@login_required
def addjob(req):
    current_user=req.user
   
    if current_user.usertype== "jobcreator":
        if req.method=="POST":
            JOB=JOOBModel()

            JOB.user=current_user
            JOB.job_title=req.POST.get('job_title')
            JOB.application_deadline=req.POST.get('application_deadline')
            JOB.company_namne=req.POST.get('company_namne')
            JOB.salary=req.POST.get('salary')
            JOB.description=req.POST.get('description')
            JOB.location=req.POST.get('location')
            JOB.ememployment_type=req.POST.get('ememployment_type')
            JOB.img=req.FILES.get('img')

            JOB.save()
            messages.success(req,"job created successfully")

            return redirect("joobfeed")

            
        return render(req,'addjob.html')

    else:
        messages.warning(req, "YOU ARE NOT A JOOBCREATOR")
        return render(req, 'common/error.html')

@login_required
def apply_now(req,apply_id):

    current_user=req.user

    if current_user.usertype== "jobseeker":

        specific_job = JOOBModel.objects.get(id=apply_id)

        text={
            "specific_job":specific_job
        }

        if req.method=="POST":
            full_name=req.POST.get('full_name')
            resume=req.POST.get('resume')
            cover=req.POST.get('cover')
            expected_salary=req.POST.get('expected_salary')
            work_experience=req.POST.get('work_experience')
            skills=req.POST.get('skills')
            linkedin_url=req.POST.get('linkedin_url')
            salary=req.POST.get('salary')

            apply=JOBAPPLYMODEL(
                user=current_user,
                job=specific_job,
                full_name=full_name,
                resume=resume,
                cover=cover,
                expected_salary=expected_salary,
                work_experience=work_experience,
                skills=skills,
                linkedin_url=linkedin_url,
                salary=salary,
            )
            apply.save()

            return redirect("joobfeed")





        return render(req,'apply_now.html', text)

    else:
        messages.warning(req,"YOU ARE NOT A JOBSEEKER")



@login_required
def changePassword(req):

    current_user = req.user

    if req.method == 'POST':
        old_password = req.POST.get('oldPassword')
        new_password = req.POST.get('newPassword')
        repeat_password = req.POST.get('repeatPassword')

        if all([old_password, new_password, repeat_password]):
            
            if check_password(old_password, current_user.password):
                if len(new_password) >= 8 and len(repeat_password):

                    current_user.set_password(new_password)
                    current_user.save()

                    #prevent logout
                    update_session_auth_hash(req,current_user)
                    messages.success(req,'Password change successfully!!')

                    return redirect('home')
                    

                else:
                    messages.success(req,'Old password is not correct!')
                    return render(req, 'change-password.html')
            else:
                messages.success(req,'Old password is not correct!')
                return render(req, 'change-password.html')
        
        else:
            messages.success(req,'All fields are required!')
            return render(req, 'change-password.html')


    return render(req, 'change-password.html')