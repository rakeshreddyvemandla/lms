from django.contrib import admin
from .models import Supervisor, Profile, Leave, LeaveType
from csvexport.actions import csvexport



@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'supervisor', 'leave_type', 'start_date', 'end_date', 'duration', 'status', 'remarks']
    list_filter = ['employee', 'supervisor', 'leave_type', 'start_date', 'end_date', 'status',]

    actions = [csvexport]

admin.site.register(Supervisor)
admin.site.register(Profile)
admin.site.register(LeaveType)

admin.site.site_title = 'Leave Management System'
admin.site.site_header = 'Leave Management Dashboard'
