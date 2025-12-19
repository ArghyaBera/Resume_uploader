import logging
import datetime
from django.shortcuts import render,redirect
from resume.models import*
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login_page/')
def rlist(request):
    if request.method=='POST':
        data=request.POST
        c_name=data.get('cand_name')
        c_gen=data.get('cand_gen')
        c_loc=data.get('cand_loc')
        c_mob=data.get('cand_mob')
        c_dob=data.get('cand_dob')
        r_pdf=request.FILES.get('res_pdf')

        if not all([c_name, c_gen, c_loc, c_mob, c_dob, r_pdf]):
            messages.error(request, 'All fields are required.')
            return redirect('/resume_list/')

        try:
            Res.objects.create(
                name=c_name,
                gender=c_gen,
                dob = c_dob,
                loc=c_loc,
                mob=c_mob,
                pdf=r_pdf
            )
        except Exception as e:
            logging.error(f"Error uploading to S3: {e}")
            messages.error(request, 'There was an error uploading your file. Please check the server logs for more details.')
            return redirect('/resume_list/')
        
        return redirect('/resume_list/')
    qset=Res.objects.all()
    return render(request,'resume_list.html', context={'r':qset})

@login_required(login_url='/login_page/')
def delete_rec(request,id):
    try:
        qset=Res.objects.get(id=id)
        qset.delete()
    except Res.DoesNotExist:
        messages.warning(request, "Record not found.")
    return redirect('/resume_list/')



@login_required(login_url='/login_page/')
def update_rec(request,id):
    try:
        qset=Res.objects.get(id=id)
    except Res.DoesNotExist:
        messages.warning(request, "Record not found.")
        return redirect('/resume_list/')
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
            qset.pdf=r_pdf
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


# ... (rest of the views rlist, delete_rec, update_rec, login_page, log_out)

def reg(request):
    if request.method=='POST':
        fname=request.POST.get('f_name')
        lname=request.POST.get('l_name')
        eml=request.POST.get('email')
        pswd=request.POST.get('pswd')
        u_name=request.POST.get('u_name')

        if not all([fname, lname, eml, pswd, u_name]):
            messages.error(request, "All fields are required.")
            return redirect('/reg_page/')

        user_by_username = User.objects.filter(username=u_name)
        user_by_email = User.objects.filter(email__iexact=eml)

        if user_by_username.exists():
            messages.info(request, "Username already exists")
            return redirect('/reg_page/')
        
        if user_by_email.exists():
            messages.info(request, "Email already exists")
            return redirect('/reg_page/')

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

@csrf_exempt
def api_upload_resume(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    r_pdf = request.FILES.get('resume_pdf')

    if not r_pdf:
        return JsonResponse({'error': 'No file provided.'}, status=400)

    try:
        # Create a new resume object with placeholder data
        new_resume = Res.objects.create(
            name="API Upload",
            gender='M',
            dob=datetime.date.today(),
            loc="N/A",
            mob=0,
            pdf=r_pdf
        )
        return JsonResponse({
            'message': 'File uploaded successfully!',
            'resume_id': new_resume.id,
            'url': new_resume.pdf.url
        })
    except Exception as e:
        logging.error(f"API Error uploading to S3: {e}")
        return JsonResponse({'error': 'An error occurred during file upload.'}, status=500)

