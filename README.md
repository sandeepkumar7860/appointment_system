


url for run the application

https://appointment-system-ckp6.onrender.com









# Appointment Booking System - Admin Dashboard

This Django application provides an appointment booking system with a comprehensive admin dashboard for managing teachers, appointments, and users.

## Features

### Admin Dashboard
- **Statistics Overview**: Total appointments, pending/granted counts, teacher count, user count
- **Recent Activity**: Last 7 days of appointments
- **Today's Schedule**: All appointments for the current day
- **Data Visualization**: Charts showing appointment status distribution and teacher popularity
- **Quick Actions**: Direct links to Django admin interface

### Enhanced Admin Interface
- **Teacher Management**: View teacher profiles with appointment counts and avatar previews
- **Appointment Management**: Advanced filtering, bulk actions (grant/reject), colored status indicators
- **User Management**: Standard Django user admin

## Setup Instructions

1. **Install Dependencies** (if not already done):
   ```bash
   pip install django
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser** (if not exists):
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## Accessing the Admin Dashboard

1. **Login as Admin/Staff User**:
   - Go to: http://127.0.0.1:8000/accounts/login/
   - Use admin credentials (username: admin, password: admin123 if using sample data)

2. **Access Admin Dashboard**:
   - URL: http://127.0.0.1:8000/admin-dashboard/
   - Only accessible to staff users

3. **Django Admin Interface**:
   - URL: http://127.0.0.1:8000/admin/
   - Full administrative control

## Sample Data

To populate the database with sample data, run:
```bash
python populate_sample_data.py
```

This will create:
- 5 sample teachers with avatars
- 1 admin user (admin/admin123)
- Multiple sample appointments with various statuses

## URLs

- `/` - Teacher list (public)
- `/admin-dashboard/` - Admin dashboard (staff only)
- `/admin/` - Django admin interface
- `/accounts/login/` - Login page
- `/accounts/logout/` - Logout
- `/register/` - User registration

## Models

### Teacher
- name: CharField
- subject: CharField
- avatar_url: URLField

### Appointment
- user: ForeignKey(User)
- teacher: ForeignKey(Teacher)
- date: DateField
- time_slot: CharField (choices: 8-9, 9-10, 10-11, 11-12)
- status: CharField (choices: pending, granted, rejected)
- message: TextField (optional)
- created_at: DateTimeField

## Admin Features

### Teacher Admin
- List display with appointment count and avatar preview
- Filtering by subject
- Search by name and subject

### Appointment Admin
- Colored status indicators
- Bulk actions: Grant appointments, Reject pending appointments
- Advanced filtering by status, teacher, date, time slot
- Date hierarchy navigation
- Field grouping in edit forms

## Security

- Admin dashboard requires `staff_member_required` decorator
- All views use Django's built-in authentication
- CSRF protection enabled
- SQL injection protection via Django ORM

## Technologies Used

- Django 5.2+
- Bootstrap 5.3 (for styling)
- SQLite (default database)
- HTML/CSS/JavaScript

## Future Enhancements

- Email notifications for appointment status changes
- Calendar view for appointments
- API endpoints for mobile app integration
- Advanced reporting and analytics
- User profile management
- Appointment reminders
