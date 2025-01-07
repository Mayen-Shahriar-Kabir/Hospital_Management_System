from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Patient')

    def __str__(self):
        return self.username

# MySQL Query corresponding to the CustomUser model creation:
# CREATE TABLE custom_user (
#     id INT AUTO_INCREMENT PRIMARY KEY,  
#     username VARCHAR(150) UNIQUE NOT NULL,  
#     first_name VARCHAR(30) NOT NULL,  
#     last_name VARCHAR(30) NOT NULL,  
#     email VARCHAR(254) UNIQUE NOT NULL,  
#     password VARCHAR(128) NOT NULL,  
#     role VARCHAR(20) NOT NULL DEFAULT 'Patient', 
#     is_staff BOOLEAN NOT NULL,  
#     is_active BOOLEAN NOT NULL,  
#     date_joined DATETIME NOT NULL,  
#     last_login DATETIME,  
#     UNIQUE (username),
#     UNIQUE (email)
# );

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    availability = models.CharField(
        max_length=20, 
        choices=[('Available', 'Available'), ('Not Available', 'Not Available')],
        default='Available'
    )
    contact = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.name}"

# The table creation query when migrating this model:

# CREATE TABLE doctor (
#     doctor_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,  
#     name VARCHAR(100),
#     speciality VARCHAR(100),
#     availability VARCHAR(20) DEFAULT 'Available',
#     contact VARCHAR(15),
#     FOREIGN KEY (user_id) REFERENCES auth_user(id)  
# );


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10) 
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# CREATE TABLE patient (
#     patient_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,  -- Foreign key linking to the user model
#     name VARCHAR(100),
#     birthdate DATE,
#     gender VARCHAR(10),
#     contact VARCHAR(15),
#     FOREIGN KEY (user_id) REFERENCES auth_user(id)  -- Assuming 'auth_user' is the table created by AUTH_USER_MODEL
# );


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=50)  
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Appointment ID: {self.appointment_id} for {self.patient.name} with Dr. {self.doctor.name}"

# MySQL Query corresponding to the Appointment model creation:
# CREATE TABLE appointment (
#     appointment_id INT AUTO_INCREMENT PRIMARY KEY,
#     date DATETIME NOT NULL,
#     status VARCHAR(50) NOT NULL,
#     doctor_id INT NOT NULL,
#     patient_id INT NOT NULL,
#     FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
#     FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
# );

class LabReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=50)  
    diagnosis = models.TextField(null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)  
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  

    def __str__(self):
        return f"Report ID: {self.report_id} for {self.patient.name}"

# MySQL Query corresponding to the LabReport model creation:
# CREATE TABLE lab_report (
#     report_id INT AUTO_INCREMENT PRIMARY KEY,
#     test_name VARCHAR(100) NOT NULL,
#     date DATE NOT NULL,
#     status VARCHAR(50) NOT NULL,
#     diagnosis TEXT,
#     cost DECIMAL(10, 2) NOT NULL,
#     patient_id INT NOT NULL,
#     FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
# );

class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name

# MySQL Query corresponding to the Admin model creation:
# CREATE TABLE admin (
#     admin_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT NOT NULL,
#     name VARCHAR(100) NOT NULL,
#     contact VARCHAR(15) NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES auth_user(id)
# );

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    date = models.DateField()
    status = models.CharField(max_length=50)  # 'Paid', 'Pending'
    criteria = models.CharField(max_length=50)  # 'Appointment' or 'Lab Report'
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Appointment (nullable)
    lab_report = models.ForeignKey(LabReport, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to LabReport (nullable)

    def save(self, *args, **kwargs):
        if not self.appointment and not self.lab_report:
            raise ValueError("A payment must be linked to either an appointment or a lab report.")
        if self.appointment and self.lab_report:
            raise ValueError("A payment cannot be linked to both an appointment and a lab report.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment ID: {self.payment_id} for {self.criteria}"

# MySQL Query corresponding to the Payment model creation:
# CREATE TABLE payment (
#     payment_id INT AUTO_INCREMENT PRIMARY KEY,
#     amount DECIMAL(10, 2) NOT NULL,
#     date DATE NOT NULL,
#     status VARCHAR(50) NOT NULL,
#     criteria VARCHAR(50) NOT NULL,
#     appointment_id INT,
#     lab_report_id INT,
#     FOREIGN KEY (appointment_id) REFERENCES appointment(appointment_id) ON DELETE CASCADE,
#     FOREIGN KEY (lab_report_id) REFERENCES lab_report(report_id) ON DELETE CASCADE
# );
