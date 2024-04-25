from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.conf import settings
from .forms import SignUpForm, EmailAuthenticationForm
from .models import Patient, Appointment,Service, Specialist, DoctorNote, PatientSummary, DentalInformation
from .forms import AppointmentForm, ServiceForm, DoctorNoteForm, PatientSummaryForm, PatientForm, DentalInformationForm
from django.http import JsonResponse
from .decorators import doctor_required, receptionist_required, admin_required

@login_required
def home(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
#####################
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@admin_required
def user_create(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Redirect to your home page
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user-list')

    return render(request, 'user_update.html', {'user': user})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user-list')
#####################

@login_required
@doctor_required
def doctor_dashboard(request):
    treated_patients = Patient.objects.filter(treated=True).order_by('-id')
    # Count treated patients
    treated_patients_count = Patient.objects.filter(treated=True).count()

    # Count appointments
    appointments_count = Appointment.objects.count()

    # Count pending patients
    pending_patients_count = Patient.objects.filter(treated=False).count()

    # Count rejected patients (if you have a field to indicate rejection)
    # rejected_patients_count = Patient.objects.filter(rejected=True).count()

    context = {
        'treated_patients': treated_patients,
        'treated_patients_count': treated_patients_count,
        'appointments_count': appointments_count,
        'pending_patients_count': pending_patients_count,
        # 'rejected_patients_count': rejected_patients_count,
    }

    return render(request, 'doctor_dashboard.html', context)

@login_required
@receptionist_required
def receptionist_dashboard(request):
    patients = Patient.objects.all()
    return render(request, 'receptionist_dashboard.html', {'patients': patients})
#####################

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient-list')
    else:
        form = PatientForm()
    return render(request, 'patient_create.html', {'form': form})

@login_required

def patient_list(request):
    patients = Patient.objects.all().order_by('-id')
    return render(request, 'patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    return render(request, 'patient_detail.html', {'patient': patient})

@login_required
def patient_update(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('doctor-dashboard')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_update.html', {'form': form, 'patient': patient})

@login_required
def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient-list')
    return render(request, 'patient_delete.html', {'patient': patient})

#####################


@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            patient_id = form.cleaned_data['patient'].id  # Extracting the patient's ID from the instance
            doctor_id = form.cleaned_data['doctor'].id  # Extracting the doctor's ID from the instance
            
            # Retrieve instances of Patient and Specialist using their IDs
            patient = get_object_or_404(Patient, id=patient_id)
            doctor = get_object_or_404(Specialist, id=doctor_id)
            
            appointment_date = form.cleaned_data['appointment_date']
            reason = form.cleaned_data['reason']
            appointment = Appointment(patient=patient, doctor=doctor, appointment_date=appointment_date, reason=reason)
            appointment.save()
            return redirect('appointment-list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_create.html', {'form': form})



@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})

####################
@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service-list')
    else:
        form = ServiceForm()
    return render(request, 'service_create.html', {'form': form})

@login_required
def service_list(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'service_list.html', context)

@login_required
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {'service': service})

@login_required
def service_update(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service-list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service_update.html', {'form': form})

@login_required
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('service-list')
    return render(request, 'service_delete.html', {'service': service})
####################

@login_required
def patient_create_note(request, patient_id):
    if request.method == 'POST':
        form = DoctorNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient-detail-note', patient_id=patient_id)
    else:
        form = DoctorNoteForm(initial={'patient': patient_id, 'doctor': request.user.id})
    return render(request, 'patient_create_note.html', {'form': form})

@login_required
def patient_detail_note(request, patient_id):
    patient_notes = DoctorNote.objects.filter(patient_id=patient_id)
    return render(request, 'patient_detail_note.html', {'patient_notes': patient_notes, 'patient_id': patient_id})

@login_required
def patient_update_note(request, note_id):
    note = get_object_or_404(DoctorNote, id=note_id)
    if request.method == 'POST':
        form = DoctorNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('patient-detail-note', patient_id=note.patient_id)
    else:
        form = DoctorNoteForm(instance=note)
    return render(request, 'patient_update_note.html', {'form': form, 'note': note})

@login_required
def patient_delete_note(request, note_id):
    note = get_object_or_404(DoctorNote, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('patient-detail-note', patient_id=note.patient_id)
    return render(request, 'patient_delete_note.html', {'note': note})
#####################

@login_required
def patient_create_summary(request, patient_id):
    if request.method == 'POST':
        form = PatientSummaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient-detail-summary', patient_id=patient_id)
    else:
        form = PatientSummaryForm(initial={'patient': patient_id})
    return render(request, 'patient_create_summary.html', {'form': form})

@login_required
def patient_detail_summary(request, patient_id):
    patient_summaries = PatientSummary.objects.filter(patient_id=patient_id)
    return render(request, 'patient_detail_summary.html', {'patient_summaries': patient_summaries, 'patient_id': patient_id})

@login_required
def patient_update_summary(request, summary_id):
    summary = get_object_or_404(PatientSummary, id=summary_id)
    if request.method == 'POST':
        form = PatientSummaryForm(request.POST, instance=summary)
        if form.is_valid():
            form.save()
            return redirect('patient-detail-summary', patient_id=summary.patient_id)
    else:
        form = PatientSummaryForm(instance=summary)
    return render(request, 'patient_update_summary.html', {'form': form, 'summary': summary})

@login_required
def patient_delete_summary(request, summary_id):
    summary = get_object_or_404(PatientSummary, id=summary_id)
    if request.method == 'POST':
        summary.delete()
        return redirect('patient-detail-summary', patient_id=summary.patient_id)
    return render(request, 'patient_delete_summary.html', {'summary': summary})
#####################

@login_required
def dental_information_create(request):
    if request.method == 'POST':
        form = DentalInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dental-info-list')
    else:
        form = DentalInformationForm()
    return render(request, 'dental_information_create.html', {'form': form})

@login_required
def dental_information_detail(request, pk):
    # dental_info = DentalInformation.objects.filter(patient_name=pk).order_by('-id')
    # idea include patient id as a link and when click it, it will show all records
    dental_info = DentalInformation.objects.filter(pk=pk).order_by('-id')
    return render(request, 'dental_information_detail.html', {'dental_info': dental_info})

@login_required
def dental_information_list(request):
    dental_info = DentalInformation.objects.all()
    return render(request, 'dental_information_list.html', {'dental_info': dental_info})

@login_required
def dental_information_update(request, pk):
    dental_info = get_object_or_404(DentalInformation, pk=pk)
    if request.method == 'POST':
        form = DentalInformationForm(request.POST, instance=dental_info)
        if form.is_valid():
            form.save()
            return redirect('dental-info-list')
    else:
        form = DentalInformationForm(instance=dental_info)
    return render(request, 'dental_information_update.html', {'form': form})

@login_required
def dental_information_delete(request, pk):
    dental_info = get_object_or_404(DentalInformation, pk=pk)
    if request.method == 'POST':
        dental_info.delete()
        return redirect('dental-info-list')
    return render(request, 'dental_information_delete.html', {'dental_info': dental_info})


