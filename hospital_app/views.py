from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Appointment, LabReport, Admin, Payment, CustomUser  
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages


def home(request):
    doctors = Doctor.objects.all()  
    context = {
        'doctors': doctors
    }
    return render(request, 'home.html', context)
# MySQL Query corresponding to the Doctor.objects.all() query:
# SELECT * FROM doctor;

# Register view
def patient_register(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        birthdate = request.POST.get('birthdate')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')

        
        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        user.role = 'Patient'  
        user.save()

        
        Patient.objects.create(
            user=user, 
            birthdate=birthdate,
            name=name,
            contact=contact,
            gender=gender
        )

        # Authenticate and login the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patient_dashboard')  
        else:
            return redirect('login')  

    return render(request, 'register.html')  

# MySQL Queries corresponding to the code:
# 1. Insert into CustomUser table (Creating a new user)
# INSERT INTO customuser (username, password, email, role) VALUES (%s, %s, %s, 'Patient');

# 2. Insert into Patient table (Creating a new patient profile)
# INSERT INTO patient (user_id, birthdate, name, contact, gender) VALUES (%s, %s, %s, %s, %s);


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'Patient':
                return redirect('patient_dashboard')
            elif user.role == 'Doctor':
                return redirect('doctor_dashboard')
            elif user.role == 'Admin':
                return redirect('admin_dashboard')
        else:
            return HttpResponse('Invalid login credentials.')

    return render(request, 'login.html')

# MySQL Query corresponding to the code:
# 1. Select user from CustomUser table based on username and password.
# SELECT * FROM customuser WHERE username = %s AND password = %s LIMIT 1;


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  


# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin':
        return redirect('home')
    payments = Payment.objects.all()
    lab_reports = LabReport.objects.all()
    if request.method == 'POST':
        if 'username' in request.POST:
            doctor_username = request.POST.get('username')  
            doctor_name = request.POST.get('name')  
            doctor_email = request.POST.get('email') 
            doctor_speciality = request.POST.get('speciality')
            doctor_availability = request.POST.get('availability')
            doctor_contact = request.POST.get('contact')
            doctor_password = request.POST.get('password')


            doctor_user = CustomUser.objects.create_user(username=doctor_username, password=doctor_password, email=doctor_email)
            doctor_user.role = 'Doctor'  
            doctor_user.save()

            doctor = Doctor.objects.create(
                user=doctor_user, 
                name=doctor_name,  
                speciality=doctor_speciality,
                availability=doctor_availability,
                contact=doctor_contact
            )

            return redirect('admin_dashboard')  
        else:
            action = request.POST.get('action')
            if action == 'mark_paid':
                payment_id = request.POST.get('payment_id')
                try:
                    payment = Payment.objects.get(payment_id=payment_id)
                    payment.status = 'Paid'
                    payment.save()
                    messages.success(request, f"Payment ID {payment_id} marked as Paid.")
                except Payment.DoesNotExist:
                    messages.error(request, "Payment not found.")

            elif action == 'mark_delivered':
                report_id = request.POST.get('report_id')
                try:
                    lab_report = LabReport.objects.get(report_id=report_id)
                    lab_report.status = 'Delivered'
                    lab_report.save()
                    messages.success(request, f"Lab Report ID {report_id} marked as Delivered.")
                except LabReport.DoesNotExist:
                    messages.error(request, "Lab report not found.")

            return redirect('admin_dashboard')
        

    return render(request, 'admin_dashboard.html', {
        'payments': payments,
        'lab_reports': lab_reports,
    })  


# MySQL Queries corresponding to the operations in the code:
# 1. Fetching all payments:
# SELECT * FROM Payment;

# 2. Fetching all lab reports:
# SELECT * FROM LabReport;

# 3. Creating a new doctor user:
# INSERT INTO CustomUser (username, password, email, role) VALUES ('doctor_username', 'doctor_password', 'doctor_email', 'Doctor');

# 4. Creating a new doctor profile:
# INSERT INTO Doctor (user_id, name, speciality, availability, contact) 
# VALUES (LAST_INSERT_ID(), 'doctor_name', 'doctor_speciality', 'doctor_availability', 'doctor_contact');

# 5. Updating payment status:
# UPDATE Payment SET status = 'Paid' WHERE payment_id = 'payment_id';

# 6. Updating lab report status:
# UPDATE LabReport SET status = 'Delivered' WHERE report_id = 'report_id';




@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor  

    appointments = Appointment.objects.filter(doctor=doctor)
    # MySQL Query: 
    # SELECT * FROM Appointment WHERE doctor_id = <doctor.id>;
    
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()
    # MySQL Query: 
    # SELECT DISTINCT * FROM Patient WHERE patient_id IN (
    #     SELECT patient_id FROM Appointment WHERE doctor_id = <doctor.id>
    # );
    lab_reports = LabReport.objects.filter(patient__in=patients).distinct()
    # MySQL Query: 
    # SELECT DISTINCT * FROM LabReport WHERE patient_id IN (
    #     SELECT DISTINCT patient_id FROM Patient WHERE patient_id IN (
    #         SELECT patient_id FROM Appointment WHERE doctor_id = <doctor.id>
    #     )
    # );
    if request.method == 'POST':
        # Update appointment status
        if 'appointment_id' in request.POST:
            appointment_id = request.POST.get('appointment_id')
            status = request.POST.get('status')
            try:
                appointment = Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
                # MySQL Query: 
                # SELECT * FROM Appointment WHERE appointment_id = <appointment_id> AND doctor_id = <doctor.id>;
                appointment.status = status
                appointment.save()
                # MySQL Query: 
                # UPDATE Appointment SET status = '<status>' WHERE appointment_id = <appointment_id>;
                messages.success(request, f'Appointment status updated to {status}!')
            except Appointment.DoesNotExist:
                messages.error(request, 'Appointment not found.')

        # Update lab report diagnosis
        elif 'lab_report_id' in request.POST:
            lab_report_id = request.POST.get('lab_report_id')
            diagnosis = request.POST.get('diagnosis')
            try:
                lab_report = LabReport.objects.get(report_id=lab_report_id, patient__in=Patient.objects.filter(appointment__doctor=doctor))
                # MySQL Query: 
                # SELECT * FROM LabReport WHERE report_id = <lab_report_id> AND patient_id IN (
                #     SELECT patient_id FROM Patient WHERE patient_id IN (
                #         SELECT patient_id FROM Appointment WHERE doctor_id = <doctor.id>
                #     )
                # );
                lab_report.diagnosis = diagnosis
                lab_report.save()
                # MySQL Query: 
                # UPDATE LabReport SET diagnosis = '<diagnosis>' WHERE report_id = <lab_report_id>;
                messages.success(request, f'Diagnosis updated for lab report ID {lab_report_id}!')
            except LabReport.DoesNotExist:
                messages.error(request, 'Lab report not found.')

        return redirect('doctor_dashboard') 

    return render(request, 'doctor_dashboard.html', {
        'appointments': appointments,
        'lab_reports': lab_reports,
    })


@login_required
def patient_dashboard(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    # MySQL Query to get the patient associated with the user
    # SELECT * FROM patient WHERE user_id = <user.id>;

    
    appointments = Appointment.objects.filter(patient=patient)
    # MySQL Query to get all appointments for the patient
    # SELECT * FROM appointment WHERE patient_id = <patient.id>;

    lab_reports = LabReport.objects.filter(patient=patient)
    # MySQL Query to get all lab reports for the patient
    # SELECT * FROM lab_report WHERE patient_id = <patient.id>;

    
    payments = Payment.objects.filter(
        Q(appointment__patient=patient) | Q(lab_report__patient=patient)
    )
    # MySQL Query to get all payments associated with the patient's appointments or lab reports
    # SELECT * FROM payment 
    # WHERE appointment_id IN (SELECT appointment_id FROM appointment WHERE patient_id = <patient.id>) 
    # OR lab_report_id IN (SELECT report_id FROM lab_report WHERE patient_id = <patient.id>);

    
    doctors = Doctor.objects.all()
    # MySQL Query to get all doctors
    # SELECT * FROM doctor;

    if request.method == 'POST':
        # appointment form submission
        if 'doctor' in request.POST and 'appointment_date' in request.POST:
            doctor_id = request.POST.get('doctor')
            appointment_date = request.POST.get('appointment_date')

            if doctor_id and appointment_date:
                try:
                    doctor = Doctor.objects.get(doctor_id=doctor_id)
                    # MySQL Query:
                    # SELECT * FROM Doctor WHERE doctor_id = <doctor_id>;

                    appointment_datetime = timezone.make_aware(datetime.strptime(appointment_date, "%Y-%m-%d"))

                    
                    appointment = Appointment.objects.create(
                        date=appointment_datetime,
                        status='Scheduled',
                        doctor=doctor,
                        patient=patient,
                    )
                    # MySQL Query:
                    # INSERT INTO Appointment (date, status, doctor_id, patient_id)
                    # VALUES (<appointment_datetime>, 'Scheduled', <doctor_id>, <patient.patient_id>);

                    Payment.objects.create(
                        amount=1000,  
                        date=datetime.today(),
                        status='Pending',
                        criteria='Appointment',
                        appointment=appointment  
                    )
                    return redirect('patient_dashboard')
                    # MySQL Query:
                    # INSERT INTO Payment (amount, date, status, criteria, appointment_id)
                    # VALUES (1000, CURDATE(), 'Pending', 'Appointment', <appointment.appointment_id>);


                except Doctor.DoesNotExist:
                    return HttpResponse("Doctor not found!", status=404)
                except Exception as e:
                    return HttpResponse(f"An error occurred: {e}", status=500)


        elif 'test_name' in request.POST:
            test_name = request.POST.get('test_name')
            fee = request.POST.get('fee')  
            current_date = timezone.now().date()  

            
            lab_report = LabReport.objects.create(
                test_name=test_name,
                date=current_date,
                status='Pending',
                diagnosis=None, 
                cost=fee,
                patient=patient
            )
            # MySQL Query:
            # INSERT INTO LabReport (test_name, date, status, diagnosis, cost, patient_id)
            # VALUES (<test_name>, CURDATE(), 'Pending', NULL, <fee>, <patient.patient_id>);


            
            Payment.objects.create(
                amount=fee,
                date=datetime.today(),
                status='Pending',
                criteria='Lab Report',
                lab_report=lab_report  
            )
            # MySQL Query:
            # INSERT INTO Payment (amount, date, status, criteria, lab_report_id)
            # VALUES (<fee>, CURDATE(), 'Pending', 'Lab Report', <lab_report.report_id>);


            return redirect('patient_dashboard')

        else:
            if request.POST.get('action') == 'request_payment':  
                payment_id = request.POST.get('payment_id')
                try:
                    payment = Payment.objects.filter(
                        Q(appointment__patient=patient) | Q(lab_report__patient=patient),
                        payment_id=payment_id
                    ).first()
                    # MySQL Query:
                    # SELECT * FROM Payment 
                    # WHERE (appointment_id IN (
                    #           SELECT appointment_id FROM Appointment WHERE patient_id = <patient.patient_id>
                    #       ) OR lab_report_id IN (
                    #           SELECT report_id FROM LabReport WHERE patient_id = <patient.patient_id>
                    #       )) AND payment_id = <payment_id>
                    # LIMIT 1;

                    if not payment:
                        raise Payment.DoesNotExist

                    payment.status = 'Requested'
                    payment.save()
                    # MySQL Query:
                    # UPDATE Payment SET status = 'Requested' WHERE payment_id = <payment_id>;
                    messages.success(request, 'Payment status updated to "Requested".')
                except Payment.DoesNotExist:
                    messages.error(request, 'Payment not found or unauthorized action.')

                return redirect('patient_dashboard') 

    return render(request, 'patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'payments': payments,
        'lab_reports': lab_reports,
        'doctors': doctors,
    })
