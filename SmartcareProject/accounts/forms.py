from django import forms
from django.contrib.auth.models import User
from . import models

#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status']

class NurseUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class NurseForm(forms.ModelForm):
    class Meta:
        model=models.Nurse
        fields=['address','mobile','department','status']
        
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','date_of_birth']


class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    nurseId=forms.ModelChoiceField(queryset=models.Nurse.objects.all().filter(status=True),empty_label="Nurse Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    appointmentDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=True) 
    appointmentTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    class Meta:
        model=models.Appointment
        fields=['appointmentTime','appointmentDate','description','status']



class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    nurseId=forms.ModelChoiceField(queryset=models.Nurse.objects.all().filter(status=True),empty_label="Nurse Name and Department", to_field_name="user_id")
    appointmentDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=True) 
    appointmentTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    class Meta:
        model=models.Appointment
        fields=['appointmentDate','appointmentTime','description','status']


