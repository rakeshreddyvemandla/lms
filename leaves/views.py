from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Leave, Supervisor, Profile, LeaveType
from .forms import LeaveForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'leaves/home.html')


def supervisor_view(request):
    form = LeaveForm()

    if request.user.is_authenticated:
        try:
            supervisor = Supervisor.objects.get(supervisor=request.user)
            if supervisor:
                leaves = Leave.objects.filter(supervisor=supervisor, status='P')
                context = {'leaves':leaves}
                return render(request, 'leaves/dashboard.html',context)
        except Supervisor.DoesNotExist:
            return HttpResponseForbidden('You are not authorizes to access this resource')

         
    return render(request, 'leaves/dashboard.html')

def employee_dashboard(request):

    if request.user.is_authenticated:
        employee = Profile.objects.get(employee=request.user)
        if employee:
            leaves = Leave.objects.filter(employee=employee).dates('start_date', 'year')
            years = [leaves.year for leaves in leaves]
            leaves = Leave.objects.filter(start_date__year__in = years, employee=employee).order_by('-start_date')
            context = {'leaves':leaves}
            return render(request, 'leaves/dashboard.html',context)
         
    return render(request, 'leaves/dashboard.html')


@login_required(login_url='login')
def leave_request(request):
    form = LeaveForm()
    employee = Profile.objects.get(employee=request.user)

    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'leaves/leave-request.html', context)
    
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            if not User.objects.get(id=employee.supervisor.id).is_active:
                error = 'Your Supervisor is not active. Please contact the admin!'
                context = {'form': form, 'error': error}
                return render(request, 'leaves/leave-request.html', context)
            
            leave.supervisor = employee.supervisor

            leave_type_id = int(request.POST.get('leave_type'))
            duration = int(request.POST.get('duration'))

            if leave_type_id == 2:  # Casual Leave
                if duration <= 12 - employee.casual_leave:
                    form.save()
                    return redirect('home')
                else:
                    error = f"You don't have enough Casual Leaves for this request. You have only {12 - employee.casual_leave} CLs left."
            elif leave_type_id == 3:  # Sick Leave
                if duration <= 6 - employee.sick_leave:
                    form.save()
                    return redirect('home')
                else:
                    error = f"You don't have enough Sick Leaves for this request. You have only {6 - employee.sick_leave} SLs left."
            elif leave_type_id == 4:  # Bereavement Leave
                if duration <= 5 - employee.bereavement_leave:
                    form.save()
                    return redirect('home')
                else:
                    error = f"You don't have enough Bereavement Leaves for this request. You have only {5 - employee.bereavement_leave} BLs left."

            elif leave_type_id == 1:
                form.save()
                return redirect('home')
            else:
                error = 'Invalid leave type'
        else:
            error = 'Invalid form submission'
        
        context = {'form': form, 'error': error}
        return render(request, 'leaves/leave-request.html', context)

        

@login_required(login_url='login')
def approve_leave(request, id):
    leave = Leave.objects.get(id=id)
    employee = Profile.objects.get(employee= User.objects.get(username=leave.employee))

    if str(leave.leave_type).lower() == 'sick leave':
        employee.sick_leave = employee.sick_leave + leave.duration
        employee.save()
     

    if str(leave.leave_type).lower() == 'bereavement leave':
        employee.bereavement_leave = employee.bereavement_leave + leave.duration
        employee.save()
     

    if str(leave.leave_type).lower() == 'casual leave':
        employee.casual_leave = employee.casual_leave + leave.duration
        employee.save()
        print(employee.casual_leave)

    leave.status = 'A'
    leave.remarks = request.POST.get('remarks')
    leave.save()
    return redirect('supervisor_view')

@login_required(login_url='login')
def reject_leave(request, id):
    leave = Leave.objects.get(id=id)
    leave.status = 'R'
    leave.remarks = request.POST.get('remarks')
    leave.save()
    return redirect('supervisor_view')


@login_required(login_url='admin')
def profile(request):
    profile = Profile.objects.get(employee=request.user)
    form = ProfileUpdateForm(instance=profile)

    context = {'form':form}

    if request.method == 'POST':
        update_profile = ProfileUpdateForm(request.POST, instance=profile)
        #update_profile.employee = request.POST.get('employee')
        update_profile.save()
        return redirect('profile-update')

    return render(request, 'leaves/profile.html', context)


def user_login(request):
    if request.method == 'GET':
        return render(request, 'leaves/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                supervisor = Supervisor.objects.get(supervisor=user)
                print(supervisor, user)
                if supervisor:
                    return redirect('supervisor_view')
            except:
                return redirect('employee_view')
            return redirect('employee_view')
        else:
            error = 'invalid username or password'
            return render(request, 'leaves/login.html', {'error':error})
