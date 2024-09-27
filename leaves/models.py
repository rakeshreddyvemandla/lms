from django.db import models
from django.contrib.auth.models import User


class Supervisor(models.Model):
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.supervisor.username



class Profile(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.IntegerField(unique=True)
    dob = models.DateField()
    contact_number = models.IntegerField()
    email = models.EmailField()
    joining_date = models.DateField()
    last_working_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True)
    casual_leave = models.IntegerField(default=0)
    sick_leave = models.IntegerField(default=0)
    optional = models.IntegerField(default=0)
    bereavement_leave = models.IntegerField(default=0)
    other_leave = models.IntegerField(default=0)
    on_duty = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.employee.username


class LeaveType(models.Model):
    leave_type = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.leave_type


class Leave(models.Model):

    _status = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )

    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField()
    status = models.CharField(choices=_status, default=_status[0][0], max_length=1)
    reason = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.employee.employee.username



