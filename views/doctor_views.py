from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from doctors.models import Blogs, Comments, Category
from users.models import Doctors, Specialty
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import json
from django.contrib.auth import get_user_model
from django.contrib import messages
from users.models import Users
from patients.models import Appointment
from pprint import pprint

User = get_user_model()

def doctor_dashboard(request):

    blogs = Blogs.objects.filter(doctor=doctor).order_by('-posted_at')
    categories = Category.objects.all()
    specialties = Specialty.objects.all()

    context = {
        'blogs': blogs,
        'categories': categories,
        'specialties': specialties,
    }

    # print(context)
    return render(request, 'admin_doctors.html', context)

def view_doctor_details(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    doctor = get_object_or_404(Doctors, user=user)

    return render(request, 'dashboard/admin_doctors_detail.html', {
        'doctor': doctor,
        'user': user,
    })  

def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password', 'default123')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        
        specialty_id = request.POST.get('specialty')
        bio = request.POST.get('bio', '')
        profile_avatar= request.FILES.get('profile_avatar')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('admin_doctor_list')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
            return redirect('admin_doctor_list')

        # 1. Buat User terlebih dahulu
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password),
            birthday=birthday,
            gender=gender,
            profile_avatar=profile_avatar,
            is_doctor=True 
        )

        # 2. Ambil Specialty
        specialty = Specialty.objects.get(id=specialty_id)

        # 3. Buat Doctor
        doctor = Doctors.objects.create(
            user=user,
            specialty=specialty,
            bio=bio,
        )
        messages.success(request, 'Doctor added successfully.')
        return redirect('admin_doctor_list')  # atau ke halaman sukses

    return redirect('admin_doctor_list')

    specialties = Specialty.objects.all()
    doctors = Doctors.objects.all()
    return render(request, 'dashboard/admin_doctors.html', {
        'specialties': specialties,
        'doctors': doctors,
    }
    )
    
@require_POST
def update_doctor(request, user_id):
    doctor = get_object_or_404(Users, id=user_id)
    user = doctor.user

    # Update user fields
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')

    # Update password jika ada
    password = request.POST.get('password')
    if password:
        user.password = make_password(password)

    user.save()

    # Update doctor fields
    doctor.birthday = request.POST.get('birthday')
    doctor.gender = request.POST.get('gender')
    doctor.specialty_id = request.POST.get('specialty')
    doctor.bio = request.POST.get('bio', '')

    # Update profile_avatar jika ada file baru
    profile_avatar = request.FILES.get('profile_avatar')
    if profile_avatar:
        doctor.profile_avatar = profile_avatar

    doctor.save()

    return redirect('admin_doctor_list')

def delete_doctor(request, user_id):
    doctor = get_object_or_404(Users, id=user_id)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully!')
    return redirect('admin_doctor_list')    

def edit_doctor(request, user_id):
    user = get_object_or_404(User, id=user_id)
    doctor = get_object_or_404(Doctors, user=user)
    specialties = Specialty.objects.all()

    return render(request, 'dashboard/admin_doctors_edit.html', {
        'user': user,
        'doctor': doctor,
        'specialties': specialties,
    })

def save_edit_doctor(request):
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    doctor = get_object_or_404(Doctors, user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.birthday = request.POST.get('birthday')
        user.gender = request.POST.get('gender')

        new_password = request.POST.get('password')
        if new_password:
            user.password = make_password(new_password)

        if 'profile_avatar' in request.FILES:
            user.profile_avatar = request.FILES['profile_avatar']

        user.save()

        specialty_id = request.POST.get('specialty')
        doctor.specialty = Specialty.objects.get(id=specialty_id)
        doctor.bio = request.POST.get('bio', '')
        doctor.save()

        messages.success(request, 'Doctor updated successfully.')
        return redirect('admin_doctor_list')

    specialties = Specialty.objects.all()

    return render(request, 'dashboard/admin_doctors_edit.html', {
        'doctor': doctor,
        'user': user,
        'specialties': specialties
    })
