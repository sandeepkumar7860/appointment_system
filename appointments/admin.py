from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Teacher, Appointment

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'appointment_count', 'avatar_preview')
    list_filter = ('subject',)
    search_fields = ('name', 'subject')

    def appointment_count(self, obj):
        return obj.appointment_set.count()
    appointment_count.short_description = 'Total Appointments'

    def avatar_preview(self, obj):
        if obj.avatar_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar_url)
        return 'No Avatar'
    avatar_preview.short_description = 'Avatar'

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher', 'date', 'time_slot', 'status_colored', 'created_at')
    list_filter = ('status', 'teacher', 'date', 'time_slot')
    search_fields = ('user__username', 'teacher__name', 'message')
    actions = ['grant_appointments', 'reject_appointments']
    date_hierarchy = 'date'
    ordering = ('-created_at',)

    def status_colored(self, obj):
        if obj.status == 'pending':
            return format_html('<span style="color: orange; font-weight: bold;">{}</span>', obj.status.title())
        elif obj.status == 'granted':
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', obj.status.title())
        return obj.status.title()
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'

    def grant_appointments(self, request, queryset):
        updated = queryset.update(status='granted')
        self.message_user(request, f'{updated} appointments granted.')
    grant_appointments.short_description = 'Grant selected appointments'

    def reject_appointments(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} pending appointments rejected.')
    reject_appointments.short_description = 'Reject selected pending appointments'

    fieldsets = (
        ('Appointment Details', {
            'fields': ('user', 'teacher', 'date', 'time_slot', 'status')
        }),
        ('Additional Information', {
            'fields': ('message', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
