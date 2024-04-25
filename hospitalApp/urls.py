from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    ##################
    path('home/', views.home, name='home'),
    ##################
    path('about/', views.about, name='about'),
    ##################
    path('contact/', views.contact, name='contact'),
    ##################
    path('user/list/', views.user_list, name='user-list'),
    path('user/create/', views.user_create, name='user-create'),
    path('user/update/<int:user_id>/', views.user_update, name='user-update'),
    path('user/delete/<int:user_id>/', views.user_delete, name='user-delete'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    ##################
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor-dashboard'),
    path('dashboard/receptionist/', views.receptionist_dashboard, name='receptionist-dashboard'),
    ##################
    path('appointment-list/', views.appointment_list, name='appointment-list'),
    path('appointments/create/', views.appointment_create, name='appointment-create'),
    ##################
    path('create/service/', views.service_create, name='service-create'),
    path('service/list/', views.service_list, name='service-list'),
    path('service/detail/<int:service_id>/', views.service_detail, name='service-detail'),
    path('<int:service_id>/update/', views.service_update, name='service-update'),
    path('<int:service_id>/delete/', views.service_delete, name='service-delete'),
    ##################
    path('patient/create/', views.patient_create, name='patient-create'),
    path('patient/list/', views.patient_list, name='patient-list'),
    path('patient/<int:patient_id>/details', views.patient_detail, name='patient-detail'),
    path('patient/<int:patient_id>/update/', views.patient_update, name='patient-update'),
    path('patient/<int:patient_id>/delete/', views.patient_delete, name='patient-delete'),
    ##################
    path('patient-create-note/<int:patient_id>/', views.patient_create_note, name='patient-create-note'),
    path('patient-detail-note/<int:patient_id>/', views.patient_detail_note, name='patient-detail-note'),
    path('patient-update-note/<int:note_id>/', views.patient_update_note, name='patient-update-note'),
    path('patient-delete-note/<int:note_id>/', views.patient_delete_note, name='patient-delete-note'),
    ##################
    path('patient-create-summary/<int:patient_id>/', views.patient_create_summary, name='patient-create-summary'),
    path('patient-detail-summary/<int:patient_id>/', views.patient_detail_summary, name='patient-detail-summary'),
    path('patient-update-summary/<int:summary_id>/', views.patient_update_summary, name='patient-update-summary'),
    path('patient-delete-summary/<int:summary_id>/', views.patient_delete_summary, name='patient-delete-summary'),
    ##################
    path('dental_info/create/', views.dental_information_create, name='dental-info-create'),
    path('dental_info/<int:pk>/detail', views.dental_information_detail, name='dental-info-detail'),
    path('dental_info/list/', views.dental_information_list, name='dental-info-list'),
    path('dental_info/<int:pk>/update/', views.dental_information_update, name='dental-info-update'),
    path('dental_info/<int:pk>/delete/', views.dental_information_delete, name='dental-info-delete'),
    ##################
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)