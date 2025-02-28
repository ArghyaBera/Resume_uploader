import email
from django.shortcuts import render,redirect
from resume.models import*
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login_page/')
def rlist(request):
    if request.method=='POST':
        data=request.POST

        c_name=data['cand_name']
        c_gen=data['cand_gen']
        c_loc=data['cand_loc']
        c_mob=data['cand_mob']
        c_dob=data['cand_dob']
        r_pdf=request.FILES.get('res_pdf')

        Res.objects.create(
            name=c_name,
            gender=c_gen,
            dob = c_dob,
            loc=c_loc,
            mob=c_mob,
            pdf=r_pdf
        )
        return redirect('/resume_list/')
    qset=Res.objects.all()
    return render(request,'resume_list.html', context={'r':qset})

@login_required(login_url='/login_page/')
def delete_rec(request,id):
    qset=Res.objects.all().get(id=id)
    qset.delete()
    return redirect('/resume_list/')



@login_required(login_url='/login_page/')
def update_rec(request,id):
    qset=Res.objects.all().get(id=id)
    if request.method=='POST':
        data=request.POST
        c_name=data['cand_name']
        c_gen=data['cand_gen']
        c_loc=data['cand_loc']
        c_mob=data['cand_mob']
        c_dob=data['cand_dob']
        r_pdf=request.FILES.get('res_pdf')

        qset.name=c_name
        qset.gender=c_gen
        qset.loc=c_loc
        qset.mob=c_mob
        qset.dob=c_dob
        if r_pdf:
            qset.img=r_pdf
        qset.save()
        return redirect('/resume_list/')

    return render(request,'updat.html',context={"rr": qset})


def login_page(request):
    if request.method == 'POST':
        eml = request.POST.get('email')
        pswd = request.POST.get('pswd')

        if not eml or not pswd:
            messages.error(request, 'Email and password are required!')
            return redirect('/login_page/')
        
        
        user = User.objects.filter(email=eml).first()

        if user is None:
            messages.error(request, 'Invalid email')  
            return redirect('/login_page/')
        
        user = authenticate(username=user.username, password=pswd)

        if user is None:
            messages.info(request, "Invalid password")
            return redirect('/login_page/')
        
        login(request, user)
        return redirect('/resume_list/')  

    return render(request, 'login_page.html')


def log_out(request):
    logout(request)
    return redirect('/login_page/')

def reg(request):
    if request.method=='POST':
        fname=request.POST.get('f_name')
        lname=request.POST.get('l_name')
        eml=request.POST.get('email')
        pswd=request.POST.get('pswd')
        u_name=request.POST.get('u_name')


        user=User.objects.filter(username=u_name)

        if user.exists():
            messages.info(request, "Username already exists")
            return redirect('/reg_page/')
        else:
            user=User.objects.create(
                first_name=fname,
                last_name=lname,
                email=eml,
                username=u_name,
            )
            user.set_password(pswd)
            user.save()
            messages.info(request, "Account created successfully")
            return redirect('/reg_page/')
          
    return render(request,'reg_page.html')

