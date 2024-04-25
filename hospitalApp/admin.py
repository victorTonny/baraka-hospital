from django.contrib import admin
from .models import Patient, Specialist, Appointment,Service, DoctorNote, PatientSummary, DentalInformation

class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('user','first_name', 'last_name', 'area_of_specialist', 'email', 'phone')
    list_filter = ('area_of_specialist', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'phone')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'gender', 'email','image', 'phone', 'body_weight', 'blood_pressure', 'pressure','receptionist','registration_time', 'treated_by', 'treated')
    list_filter = ('gender',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    
    
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'is_confirmed')
    list_filter = ('is_confirmed',)
    search_fields = ('patient__username', 'doctor__username', 'appointment_date')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','description')
    list_filter = ('name', 'price')
    search_fields = ('name', 'description')
    
class DoctorNoteAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'note_date', 'symptoms')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')



class PatientSummaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'summary_note']
    search_fields = ['service', 'patient__first_name', 'patient__last_name']

    def service_name(self, obj):
        return obj.service.name

class DentalInformationAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'last_dental_visit')
    search_fields = ('patient_name',)

admin.site.register(DentalInformation, DentalInformationAdmin)
admin.site.register(PatientSummary, PatientSummaryAdmin)
admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(DoctorNote, DoctorNoteAdmin)
