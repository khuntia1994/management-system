from django.shortcuts import render, HttpResponse, redirect
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q
from django.contrib import messages
from django.db import connection

def index(request):
    """
    Handles admin login.
    """
    if request.method == 'POST':
        # Get the form data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username is "admin" and the password is "12345"
        if username == "admin" and password == "12345":
            # Simulate a successful login
            return redirect('all_emp')  # Redirect to 'all_emp'
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'index.html')

def all_emp(request):
    """
    View to display all employees without updating row numbers.
    """
    try:
        # Fetch all employees ordered by ID (or row_number if it exists)
        emps = Employee.objects.all().order_by('id')
    except Exception as e:
        messages.error(request, f"Error fetching employees: {e}")
        emps = []

    # Render the template with employee data
    return render(request, 'view_all_emp.html', {'emps': emps})


def add_emp(request):
    """
    Handles adding a new employee via POST and updates row numbers in sequential order.
    """
    if request.method == 'POST':
        try:
            # Retrieve form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = int(request.POST.get('phone', 0))
            salary = int(request.POST.get('salary', 0))
            bonus = int(request.POST.get('bonus', 0))
            dept_id = int(request.POST.get('dept', 0))
            role_id = int(request.POST.get('role', 0))
            
            #Phone number validation
            phone_str = str(phone)  # Ensure phone is treated as a string
            if not phone_str.isdigit() or len(phone_str) < 10 or len(phone_str) > 12:
                raise ValueError("Phone number must is incorrect.")

            # Validate form data
            if not first_name or not last_name:
                raise ValueError("First name and last name are required.")
            
            # Fetch Department and Role objects
            dept = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)

            # Save the new employee
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                salary=salary,
                bonus=bonus,
                dept=dept,
                role=role,
                hire_date=datetime.now()
            )
            new_emp.save()

            # Reassign row numbers sequentially
            employees = Employee.objects.all().order_by('id')  # Ensure proper order
            for index, emp in enumerate(employees, start=1):
                emp.row_number = index
                emp.save(update_fields=['row_number'])

            messages.success(request, 'Employee added successfully!')
            return redirect('all_emp')

        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect('add_emp')
    
    elif request.method == 'GET':
        try:
            # Fetch departments and roles for dropdowns
            departments = Department.objects.all()
            roles = Role.objects.all()
            context = {'departments': departments, 'roles': roles}
            return render(request, 'add_emp.html', context)  # This line ensures you return an HttpResponse

        except Exception as e:
            messages.error(request, f"Error loading form: {e}")
            return redirect('index')

    else:
        return HttpResponse("Method not allowed.", status=405)




def remove_emp(request, emp_id=0):
    """
    Handles removing an employee by ID and reassigning row numbers after deletion.
    """
    if emp_id:
        try:
            # Find and remove the employee
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()

            messages.success(request, "Employee removed successfully.")
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found.")
        return redirect('all_emp')  # Redirect to the updated list page
    else:
        emps = Employee.objects.all()
        context = {'emps': emps}
        return render(request, 'remove_emp.html', context)

def filter_emp(request):
    """
    Filters employees based on name, department, or role.
    """
    # For debugging: print request method
    print(f"Request Method: {request.method}")

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        dept = request.POST.get('dept', '').strip()
        role = request.POST.get('role', '').strip()

        # For debugging: print the filters being used
        print(f"Filtering with Name: {name}, Department: {dept}, Role: {role}")

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name=dept)
        if role:
            emps = emps.filter(role__name=role)


        context = {
            'emps': emps,  # Pass the filtered employees
            'name': name,       # Pass the filter criteria
            'dept': dept,
            'role': role,
            'departments': Department.objects.all(),  # Include all departments for dropdowns
            'roles': Role.objects.all()  # Include all roles for dropdowns
        }

        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        context = {
            'departments': Department.objects.all(),  # Include all departments for dropdowns
            'roles': Role.objects.all()  # Include all roles for dropdowns
        }
        return render(request, 'filter_emp.html', context)




