from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Teacher, Appointment

def home(request):
    """Home page with login options"""
    return render(request, 'appointments/home.html')

def user_login(request):
    """Unified login for students and staff"""
    if request.user.is_authenticated:
        # Redirect based on user role
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('teacher_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            # Redirect based on user role
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('teacher_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/user_login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure new users are regular students, not staff
            user.is_staff = False
            user.save()

            # Add the user to 'student' group (create group if needed)
            student_group, created = Group.objects.get_or_create(name='student')
            user.groups.add(student_group)

            messages.success(request, 'Account created successfully! Please log in as a student.')
            return redirect('user_login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'appointments/teacher_list.html', {'teachers': teachers})

@login_required
def book_appointment(request, teacher_id):
    # Prevent staff/admin accounts from booking student appointments
    if request.user.is_staff:
        messages.error(request, 'Staff accounts cannot book student appointments. Use the admin interface to manage appointments.')
        return redirect('admin_dashboard')

    # Ensure user is a member of the 'student' group
    if not request.user.groups.filter(name='student').exists():
        messages.error(request, 'Only student accounts are allowed to book appointments. Please register or contact admin.')
        return redirect('teacher_list')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        time_slot = request.POST.get('time_slot')
        date = request.POST.get('date')
        if time_slot and date:
            Appointment.objects.create(user=request.user, teacher=teacher, time_slot=time_slot, date=date)
            messages.success(request, 'Appointment booked successfully!')
            return redirect('teacher_list')
    return render(request, 'appointments/book_appointment.html', {'teacher': teacher})

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})

@login_required
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'appointments/teacher_detail.html', {'teacher': teacher})

@login_required
def chatbot(request):
    teachers = Teacher.objects.all()
    return render(request, 'appointments/chatbot.html', {'teachers': teachers})

@staff_member_required
def admin_dashboard(request):
    # Get statistics
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    granted_appointments = Appointment.objects.filter(status='granted').count()
    total_teachers = Teacher.objects.count()
    total_users = User.objects.count()

    # Recent appointments (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_appointments = Appointment.objects.filter(created_at__gte=seven_days_ago).order_by('-created_at')[:10]

    # Appointments by status
    appointments_by_status = Appointment.objects.values('status').annotate(count=Count('status'))

    # Appointments by teacher
    appointments_by_teacher = Appointment.objects.values('teacher__name').annotate(count=Count('teacher')).order_by('-count')[:5]

    # Today's appointments
    today = timezone.now().date()
    todays_appointments = Appointment.objects.filter(date=today).order_by('time_slot')

    context = {
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'granted_appointments': granted_appointments,
        'total_teachers': total_teachers,
        'total_users': total_users,
        'recent_appointments': recent_appointments,
        'appointments_by_status': appointments_by_status,
        'appointments_by_teacher': appointments_by_teacher,
        'todays_appointments': todays_appointments,
    }

    return render(request, 'appointments/admin_dashboard.html', context)

@staff_member_required
def manage_appointments(request):
    """View all appointments and manage their status"""
    filter_status = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    appointments = Appointment.objects.all().order_by('-date', 'time_slot')
    
    # Filter by status
    if filter_status != 'all':
        appointments = appointments.filter(status=filter_status)
    
    # Search by user or teacher
    if search_query:
        appointments = appointments.filter(
            Q(user__username__icontains=search_query) | 
            Q(teacher__name__icontains=search_query)
        )
    
    context = {
        'appointments': appointments,
        'filter_status': filter_status,
        'search_query': search_query,
    }
    
    return render(request, 'appointments/manage_appointments.html', context)

@staff_member_required
def approve_appointment(request, appointment_id):
    """Approve or reject an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        message = request.POST.get('message', '')
        
        if action == 'approve':
            appointment.status = 'granted'
            appointment.message = message
            appointment.save()
            messages.success(request, f'Appointment approved for {appointment.user.username}!')
        elif action == 'reject':
            appointment.status = 'rejected'
            appointment.message = message
            appointment.save()
            messages.success(request, f'Appointment rejected for {appointment.user.username}!')
        
        return redirect('manage_appointments')
    
    context = {
        'appointment': appointment,
    }
    
    return render(request, 'appointments/approve_appointment.html', context)
