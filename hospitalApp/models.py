from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
WORK_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Receptionist', 'Receptionist'),
    ]


class CommonFields(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='profile_images/', default='default/default.jpg')
    class Meta:
        abstract = True  # This is an abstract base class to share common fields

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Specialist(CommonFields):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area_of_specialist = models.CharField(max_length=50, choices=WORK_CHOICES)

class Patient(CommonFields):
    body_weight = models.DecimalField(max_digits=5, decimal_places=2)  # Example: DecimalField for body weight
    blood_pressure = models.CharField(max_length=15)  # Example: CharField for blood pressure
    pressure = models.CharField(max_length=15)  # Example: CharField for pressure
    receptionist = models.ForeignKey(Specialist, on_delete=models.CASCADE, limit_choices_to={'area_of_specialist': 'Receptionist'})
    registration_time = models.DateTimeField(auto_now_add=True)
    treated_by = models.ForeignKey(Specialist, on_delete=models.CASCADE, limit_choices_to={'area_of_specialist': 'Doctor'}, related_name='patients_treated')
    treated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment for {self.patient.first_name} on {self.appointment_date}'

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class DoctorNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    note_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    
    def is_doctor(self):
        return self.doctor.area_of_specialist == 'Doctor'

    def __str__(self):
        specialist_type = "Doctor" if self.is_doctor() else "Receptionist"
        return f"Note for {self.patient.first_name} by {specialist_type} {self.doctor.first_name} on {self.note_date}"

class PatientSummary(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    summary_date = models.DateTimeField(auto_now_add=True)
    summary_note = models.TextField()

    def __str__(self):
        return f"Summary for {self.patient.first_name} on {self.summary_date}"

class DentalInformation(models.Model):
    patient_name = models.ForeignKey(Patient, on_delete=models.CASCADE)
    last_dental_visit = models.DateTimeField(blank=True, null=True)
    dental_procedures = models.TextField(blank=True)
    brushing_frequency = models.CharField(max_length=50, blank=True)
    flossing_frequency = models.CharField(max_length=50, blank=True)
    toothpaste_used = models.CharField(max_length=100, blank=True)
    mouthwash_used = models.CharField(max_length=100, blank=True)
    experiencing_discomfort = models.BooleanField(default=False)
    sensitivity_description = models.TextField(blank=True)
    gum_bleeding = models.BooleanField(default=False)
    gum_swelling = models.BooleanField(default=False)
    gum_tenderness = models.BooleanField(default=False)
    gum_changes_description = models.TextField(blank=True)
    sugary_food_frequency = models.CharField(max_length=50, blank=True)
    acidic_food_frequency = models.CharField(max_length=50, blank=True)
    impacting_habits = models.TextField(blank=True)
    medications_impacting_oral_health = models.TextField(blank=True)
    medical_conditions_impacting_dental_care = models.TextField(blank=True)
    cosmetic_interests = models.TextField(blank=True)
    oral_care_guidance = models.TextField(blank=True)
    routine_checkup_due = models.BooleanField(default=False)

    def __str__(self):
        return f"Dental Information for {self.patient_name}"
