from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from . import forms,models
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.http import JsonResponse
from .models import Doctor, Nurse


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'smartcare/home.html')

#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'smartcare/adminclick.html')


#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'smartcare/doctorclick.html')


#for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'smartcare/patientclick.html')

#for showing signup/login button for nurse
def nurseclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'smartcare/nurseclick.html')

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'smartcare/adminsignup.html',{'form':form})


def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'smartcare/doctorsignup.html',context=mydict)




#-----------for checking user is doctor , patient, nurse or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_nurse(user):
    return user.groups.filter(name='NURSE').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR, NURSE OR PATIENT

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'smartcare/doctor_wait_for_approval.html')
    
    elif is_nurse(request.user):
        accountapproval=models.Nurse.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('nurse-dashboard')
        else:
            return render(request,'smartcare/nurse_wait_for_approval.html')

    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'smartcare/patient_wait_for_approval.html')



def fetch_names(request):
    role = request.GET.get('role')
    if role == 'doctor':
        doctors = Doctor.objects.all().values('id', 'user__first_name', 'user__last_name')
        data = [{'id': doctor['id'], 'name': f"{doctor['user__first_name']} {doctor['user__last_name']}"} for doctor in doctors]
    elif role == 'nurse':
        nurses = Nurse.objects.all().values('id', 'user__first_name', 'user__last_name')
        data = [{'id': nurse['id'], 'name': f"{nurse['user__first_name']} {nurse['user__last_name']}"} for nurse in nurses]
    else:
        data = []
    return JsonResponse(data, safe=False)



#---------------------------------------------------------------------------------
#------------------------ ADMIN VIEWS  ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    nurses=models.Nurse.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    nursecount=models.Nurse.objects.all().filter(status=True).count()
    pendingnursecount=models.Nurse.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'nurses':nurses,
    'doctorcount':doctorcount,
    'nursecount':nursecount,
    'pendingnursecount':pendingnursecount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'smartcare/admin_dashboard.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'smartcare/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'smartcare/admin_view_doctor.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'smartcare/admin_update_doctor.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'smartcare/admin_add_doctor.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'smartcare/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')


#---------------------------------------------------------------------------------
#------------------ADMIN APPOINTMENT VIEWS#------------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'smartcare/admin_appointment.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    for appointment in appointments:
        appointment.doctorName = models.User.objects.get(id=appointment.doctorId).first_name
        appointment.patientName = models.User.objects.get(id=appointment.patientId).first_name
    return render(request, 'smartcare/admin_view_appointment.html', {'appointments': appointments})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.nurseId=request.POST.get('nurseId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.nurseName=models.User.objects.get(id=request.POST.get('nurseId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'smartcare/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'smartcare/admin_approve_appointment.html',{'appointments':appointments})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_appointment(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-view-appointment')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointmentForm=forms.AppointmentForm()

    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
            return redirect('admin-view-appointment')
    return render(request,'smartcare/admin_update_appointment.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointmentForm=forms.AppointmentForm()
    
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
            return redirect('admin-view-appointment')
    return render(request,'smartcare/admin_update_appointment.html',context=mydict)


#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    # for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'smartcare/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'smartcare/doctor_patient.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'smartcare/doctor_view_patient.html',
                  {'patients':patients,'doctor':doctor} 
                  )


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'smartcare/doctor_view_discharge_patient.html'
                  ,{'dischargedpatients':dischargedpatients,'doctor':doctor} 
                  )

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'smartcare/doctor_appointment.html',{'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id) 
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid) 
    appointments=zip(appointments,patients) 
    return render(request,'smartcare/doctor_view_appointment.html',
                  {'appointments':appointments,'doctor':doctor} 
                  )


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'smartcare/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})




#  ask teacher about it ! 
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'smartcare/doctor_delete_appointment.html',{
        'appointments':appointments,'doctor':doctor
        })



#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'smartcare/patientsignup.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'smartcare/admin_patient.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'smartcare/admin_view_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'smartcare/admin_update_patient.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
           
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'smartcare/admin_add_patient.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'smartcare/admin_approve_patient.html',{'patients':patients})


@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    appointments = models.Appointment.objects.filter(status=True)
    patients = models.Patient.objects.filter(status=True)

    for appointment in appointments:
        appointment.doctorName = models.User.objects.get(id=appointment.doctorId).first_name
        appointment.patientName = models.User.objects.get(id=appointment.patientId).first_name

    mydic = {
        'appointments': appointments,
        'patients': patients
    }

    return render(request, 'smartcare/admin_discharge_patient.html', context=mydic)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    pDD=models.PatientDischargeDetails()
    appointments = models.Appointment.objects.all().filter(status=True)
    for appointment in appointments:
        appointment.doctorName = models.User.objects.get(id=appointment.doctorId).first_name
        appointment.patientName = models.User.objects.get(id=appointment.patientId).first_name

    
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
        'appointments': appointments,
        'patients': patient
    }
    
    if request.method == 'POST':
        feeDict ={
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }

        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms 
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'smartcare/patient_final_bill.html',context=patientDict,)
    return render(request,'smartcare/patient_generate_bill.html',context=patientDict,)


#--------------for discharge patient bill (pdf) download and printing

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('smartcare/download_bill.html',dict)


#---------------------------------------------------------------------------------
#------------------------ INVOICE VIEWS  ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_invoice_view(request):
    invoices=models.PatientDischargeDetails.objects.all().filter()
    return render(request,'smartcare/admin_view_invoice.html',{'invoices':invoices})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_invoice_download(request,pk):
    patient = models.Patient.objects.get(id=pk)  # Fetch patient based on the provided pk
    invoices = models.PatientDischargeDetails.objects.filter(patientId=patient.id).order_by('-id')[:1]
    return render(request, 'smartcare/download_bill.html', {'invoices': invoices})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_invoice(request,pk):
    invoices=models.PatientDischargeDetails.objects.all().filter()
    invoices.delete()
    return redirect('admin-view-invoices')


# -------------------------------------------------
# ___________PATIENT RELATED_________________
# -------------------------------------------------

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'smartcare/patient_dashboard.html',context=mydict)

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'smartcare/patient_appointment.html',{'patient':patient})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.nurseId=request.POST.get('nurseId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.nurseName=models.User.objects.get(id=request.POST.get('nurseId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'smartcare/patient_book_appointment.html',context=mydict)

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'smartcare/patient_view_appointment.html',{'appointments':appointments,'patient':patient})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'smartcare/patient_discharge.html',context=patientDict)

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_delete_appointment(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('patient-view-appointment')

#---------------------------------------------------------------------------------
#------------------------ NURSE VIEWS  ------------------------------
#---------------------------------------------------------------------------------

def nurse_signup_view(request):
    userForm=forms.NurseUserForm()
    nurseForm=forms.NurseForm()
    mydict={'userForm':userForm,'nurseForm': nurseForm}
    if request.method=='POST':
        userForm=forms.NurseUserForm(request.POST)
        nurseForm=forms.NurseForm(request.POST,request.FILES)
        if userForm.is_valid() and nurseForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            nurse=nurseForm.save(commit=False)
            nurse.user=user
            nurse=nurse.save()
            my_nurse_group = Group.objects.get_or_create(name='NURSE')
            my_nurse_group[0].user_set.add(user)
        return HttpResponseRedirect('nurselogin')
    return render(request,'smartcare/nursesignup.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_nurse_view(request):
    return render(request,'smartcare/admin_nurse.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_nurse_view(request):
    nurses=models.Nurse.objects.all().filter(status=True)
    return render(request,'smartcare/admin_view_nurse.html',{'nurses':nurses})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_nurse_from_hospital_view(request,pk):
    nurse=models.Nurse.objects.get(id=pk)
    user=models.User.objects.get(id=nurse.user_id)
    user.delete()
    nurse.delete()
    return redirect('admin-view-nurse')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_nurse_view(request,pk):
    nurse=models.Nurse.objects.get(id=pk)
    user=models.User.objects.get(id=nurse.user_id)

    userForm=forms.NurseUserForm(instance=user)
    nurseForm=forms.NurseForm(request.FILES,instance=nurse)
    mydict={'userForm':userForm,'nurseForm':nurseForm}
    if request.method=='POST':
        userForm=forms.NurseUserForm(request.POST,instance=user)
        nurseForm=forms.NurseForm(request.POST,request.FILES,instance=nurse)
        if userForm.is_valid() and nurseForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            nurse=nurseForm.save(commit=False)
            nurse.status=True
            nurse.save()
            return redirect('admin-view-nurse')
    return render(request,'smartcare/admin_update_nurse.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_nurse_view(request):
    userForm=forms.NurseUserForm()
    nurseForm=forms.NurseForm()
    mydict={'userForm':userForm,'nurseForm':nurseForm}
    if request.method=='POST':
        userForm=forms.NurseUserForm(request.POST)
        nurseForm=forms.NurseForm(request.POST, request.FILES)
        if userForm.is_valid() and nurseForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            nurse=nurseForm.save(commit=False)
            nurse.user=user
            nurse.status=True
            nurse.save()

            my_nurse_group = Group.objects.get_or_create(name='NURSE')
            my_nurse_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-nurse')
    return render(request,'smartcare/admin_add_nurse.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_nurse_view(request):
    #those whose approval are needed
    nurses=models.Nurse.objects.all().filter(status=False)
    return render(request,'smartcare/admin_approve_nurse.html',{'nurses':nurses})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_nurse_view(request,pk):
    nurse=models.Nurse.objects.get(id=pk)
    nurse.status=True
    nurse.save()
    return redirect(reverse('admin-approve-nurse'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_nurse_view(request,pk):
    nurse=models.Nurse.objects.get(id=pk)
    user=models.User.objects.get(id=nurse.user_id)
    user.delete()
    nurse.delete()
    return redirect('admin-approve-nurse')

@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedNurseId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,nurseId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedNurseName=request.user.first_name).count()
   
    # for  table in nurse dashboard
    appointments=models.Appointment.objects.all().filter(status=True,nurseId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'nurse':models.Nurse.objects.get(user_id=request.user.id),
    }
    return render(request,'smartcare/nurse_dashboard.html',context=mydict)

@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_patient_view(request):
    mydict={
    'nurse':models.Nurse.objects.get(user_id=request.user.id), #for profile picture of nurse in sidebar
    }
    return render(request,'smartcare/nurse_patient.html',context=mydict)


@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedNurseId=request.user.id)
    nurse=models.Nurse.objects.get(user_id=request.user.id) 
    return render(request,'smartcare/nurse_view_patient.html',
                  {'patients':patients,'nurse':nurse} 
                  )

@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedNurseName=request.user.first_name)
    nurse=models.Nurse.objects.get(user_id=request.user.id)
    return render(request,'smartcare/nurse_view_discharge_patient.html'
                  ,{'dischargedpatients':dischargedpatients,'nurse':nurse} 
                  )

@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_appointment_view(request):
    nurse=models.Nurse.objects.get(user_id=request.user.id)
    return render(request,'smartcare/nurse_appointment.html',{'nurse':nurse})

@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_view_appointment_view(request):
    nurse=models.Nurse.objects.get(user_id=request.user.id) 
    appointments=models.Appointment.objects.all().filter(status=True,nurseId=request.user.id) 
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
        patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid) 
        appointments=zip(appointments,patients) 
    return render(request,'smartcare/nurse_view_appointment.html',
                  {'appointments':appointments,'nurse':nurse} 
                  )

@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_delete_appointment_view(request):
    nurse=models.Nurse.objects.get(user_id=request.user.id) #for profile picture of nurse in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,nurseId=request.user.id)
    patientid=[]
    for a in appointments:                   
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'smartcare/nurse_delete_appointment.html',
                  {'appointments':appointments,'nurse':nurse}
                  )

@login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    nurse=models.Nurse.objects.get(user_id=request.user.id) 
    appointments=models.Appointment.objects.all().filter(status=True,nurseId=request.user.id)
    patientid=[]
    for a in appointments:                         
        patientid.append(a.patientId)
        patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
        appointments=zip(appointments,patients)
    return render(request,'smartcare/nurse_delete_appointment.html',
                  {'appointments':appointments,'nurse':nurse} 
                  )



