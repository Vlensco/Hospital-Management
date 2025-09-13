from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from views import admin_views, doctor_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('doctors.urls')),
    path('', include('patients.urls')),
    path('users/', include('users.urls')),
    path('users/admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),


    path('users/admin/doctors/', admin_views.admin_doctor_list, name='admin_doctor_list'),
    path('users/admin/patients/', admin_views.admin_patient_list, name='admin_patient_list'),
    path('users/admin/users/', admin_views.admin_user_list, name='admin_user_list'),

    path('users/admin/login/', admin_views.admin_login, name='admin_login'),
    path('users/admin/logout/', admin_views.admin_logout, name='admin_logout'),

    path('users/admin/doctors/add/', doctor_views.add_doctor, name='add_doctor'),
    path('users/admin/doctors/details/<int:user_id>', doctor_views.view_doctor_details, name='view_doctor_details'),
    path('users/admin/doctors/update/<int:user_id>/', doctor_views.update_doctor, name='update_doctor'),
    path('users/admin/doctors/delete/<int:user_id>/', doctor_views.delete_doctor, name='delete_doctor'),  
    path('users/admin/doctors/edit/<int:user_id>/', doctor_views.edit_doctor, name='edit_doctor'),
    path('users/admin/doctors/saveedit/', doctor_views.save_edit_doctor, name='save_edit_doctor'),  
 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
