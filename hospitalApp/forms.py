from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Appointment, Service, DoctorNote, PatientSummary, Patient, DentalInformation

class BootstrapStyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control col-md-12'})
            
class SignUpForm(UserCreationForm, BootstrapStyleForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control', 'placeholder':'use your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'enter password'}))
    class Meta:
        fields = ['username', 'password']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'reason', 'is_confirmed']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control col-md-6'}),  # Apply Bootstrap styling to the patient field
            'doctor': forms.Select(attrs={'class': 'form-control col-md-6'}),  # Apply Bootstrap styling to the doctor field
            'appointment_date': forms.DateInput(attrs={'class': 'form-control col-md-6', 'type': 'date'}),  # Apply Bootstrap styling to the date field
            'reason': forms.Textarea(attrs={'class': 'form-control col-md-6', 'rows': 3}),  # Apply Bootstrap styling to the reason field
            'is_confirmed': forms.CheckboxInput(attrs={'class': 'form-check-input col-md-1'}),  # Apply Bootstrap styling to the checkbox widget
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
    }

    labels = {
        'name': 'Service Name',
        'description': 'Description',
        'price': 'Price',
    }

class DoctorNoteForm(forms.ModelForm):
    class Meta:
        model = DoctorNote
        fields = ['patient', 'doctor', 'symptoms']
        widgets = {
            'patient': forms.HiddenInput(),
            'doctor': forms.HiddenInput(),
        }

class PatientSummaryForm(forms.ModelForm):
    class Meta:
        model = PatientSummary
        fields = ['service', 'summary_note']

    def __init__(self, *args, **kwargs):
        super(PatientSummaryForm, self).__init__(*args, **kwargs)
        # You can customize the form fields if needed
        self.fields['service'].widget.attrs.update({'class': 'form-control'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control', 'rows': '4'})

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['registration_time']  # Exclude the non-editable field

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
            'age': forms.NumberInput(attrs={'class': 'form-control col-md-5'}),
            'gender': forms.Select(attrs={'class': 'form-control col-md-5'}),
            'address': forms.Textarea(attrs={'class': 'form-control col-md-5', 'rows': 1}),
            'phone': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
            'email': forms.EmailInput(attrs={'class': 'form-control col-md-5'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control col-md-5'}),
            'body_weight': forms.NumberInput(attrs={'class': 'form-control col-md-5'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
            'pressure': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
            'receptionist': forms.Select(attrs={'class': 'form-control col-md-5'}),
            'treated_by': forms.Select(attrs={'class': 'form-control col-md-5'}),
            'treated': forms.CheckboxInput(attrs={'class': 'form-check-input col-md-1'}),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'age': 'Age',
            'gender': 'Gender',
            'address': 'Address',
            'phone': 'Phone',
            'email': 'Email',
            'image': 'Profile Image',
            'body_weight': 'Body Weight',
            'blood_pressure': 'Blood Pressure',
            'pressure': 'Pressure',
            'receptionist': 'Receptionist',
            'treated_by': 'Treated By',
            'treated': 'Is Treated?',
        }

class DentalInformationForm(forms.ModelForm):
    class Meta:
        model = DentalInformation
        fields = '__all__'
        labels = {
            'patient_name': 'Jina la Mgonjwa',
            'last_dental_visit': 'Tarehe ya Mgonjwa Kupelekwa Kliniki ya Meno Mwisho',
            'dental_procedures': 'Taratibu za Kliniki ya Meno za Zamani',
            'brushing_frequency': 'Ufutaji wa Meno Kila Siku',
            'flossing_frequency': 'Kufua Meno Kila Siku',
            'toothpaste_used': 'Aina ya Dawa ya Meno Inayotumiwa',
            'mouthwash_used': 'Aina ya Kinywa cha Kutumia',
            'experiencing_discomfort': 'Unakumbana na Maumivu au Udhia wa Aina Yoyote ya Meno?',
            'sensitivity_description': 'Maelezo ya Ufahamu wa Meno Kwa Joto, Baridi, au Vyakula Vitamu',
            'gum_bleeding': 'Unakumbana na Damu katika Fizi?',
            'gum_swelling': 'Unakumbana na Kuvimba kwa Fizi?',
            'gum_tenderness': 'Unakumbana na Maumivu kwenye Fizi?',
            'gum_changes_description': 'Maelezo ya Mabadiliko kwenye Fizi',
            'sugary_food_frequency': 'Maradufu ya Vyakula Vyenye Sukari',
            'acidic_food_frequency': 'Maradufu ya Vyakula Vyenye Asidi',
            'impacting_habits': 'Mazoea Yanayoathiri Afya ya Meno',
            'medications_impacting_oral_health': 'Dawa Zinazoweza Kuathiri Afya ya Meno',
            'medical_conditions_impacting_dental_care': 'Hali za Kimsingi Zinazoweza Kuathiri Matibabu ya Meno',
            'cosmetic_interests': 'Mipango ya Urembo wa Meno',
            'oral_care_guidance': 'Ushauri wa Uangalizi wa Meno',
            'routine_checkup_due': 'Unahitaji Ziara ya Kawaida ya Uchunguzi?',
        }
        widgets = {
        'patient_name': forms.Select(attrs={'class': 'form-control col-md-5'}),
        'last_dental_visit': forms.DateInput(attrs={'type': 'date', 'class': 'form-control col-md-5'}),
        'dental_procedures': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'brushing_frequency': forms.TextInput(attrs={'placeholder': 'Mara ngapi kwa siku?', 'class': 'form-control col-md-5'}),
        'flossing_frequency': forms.TextInput(attrs={'placeholder': 'Mara ngapi kwa siku?', 'class': 'form-control col-md-5'}),
        'toothpaste_used': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
        'mouthwash_used': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
        'experiencing_discomfort': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'sensitivity_description': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'gum_bleeding': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'gum_swelling': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'gum_tenderness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'gum_changes_description': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'sugary_food_frequency': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
        'acidic_food_frequency': forms.TextInput(attrs={'class': 'form-control col-md-5'}),
        'impacting_habits': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'medications_impacting_oral_health': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'medical_conditions_impacting_dental_care': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'cosmetic_interests': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'oral_care_guidance': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control col-md-5'}),
        'routine_checkup_due': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }

