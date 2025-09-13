from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Doctors, Patients, Users, Specialty
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from users.models import Doctors, Patients
from doctors.models import Blogs, Comments, Category
from patients.models import Appointment
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator


def admin_dashboard(request):
    total_doctors = Doctors.objects.count()
    total_patients = Patients.objects.count()
    total_users = Users.objects.count()
    total_specialties = Specialty.objects.count()
    recent_appointments = Appointment.objects.select_related('doctor__user', 'patient__user', 'status').order_by('-start_date')[:5]
    total_blogs = Blogs.objects.count()
    total_appointments = Appointment.objects.count()


    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_users': total_users,
        'total_specialties': total_specialties,
        'recent_appointments': recent_appointments,
        'total_blogs': total_blogs,
        'total_appointments' : total_appointments

    }
    return render(request, 'dashboard/admin_dashboard.html', context)

def admin_doctor_list(request):
    # --- Doctors Pagination ---
    doctors_list = Doctors.objects.annotate(
        appointment_count=Count('appointment'),
    ).select_related('user')
    doctor_paginator = Paginator(doctors_list, 5)
    doctor_page_number = request.GET.get('doctor_page')
    doctors = doctor_paginator.get_page(doctor_page_number)

    # --- Blogs Pagination ---
    blogs_list = Blogs.objects.all().order_by('-posted_at')
    blog_paginator = Paginator(blogs_list, 3)
    blog_page_number = request.GET.get('blog_page')
    blogs = blog_paginator.get_page(blog_page_number)

    categories = Category.objects.all()
    specialties = Specialty.objects.all()

    context = {
        'doctors': doctors,
        'blogs': blogs,
        'categories': categories,
        'specialties': specialties,
    }

    return render(request, 'dashboard/admin_doctors.html', context)



def admin_patient_list(request):
    patients = Patients.objects.select_related('user').all()
    return render(request, 'dashboard/admin_patients.html', {'patients': patients})

def admin_user_list(request):
    users = Users.objects.all()
    return render(request, 'dashboard/admin_users.html', {'users': users})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {username}!')
            return redirect('admin_dashboard')  # <- Redirect ke dashboard
        else:
            messages.error(request, 'Username atau password salah.')
            return redirect('admin_login')
    return render(request, 'auth/admin_login.html')


@csrf_exempt
def admin_logout(request):
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        messages.success(request, f"Anda berhasil logout, {username}.")
        return redirect('/users/admin/login/')
    return redirect('/users/admin/dashboard/')
