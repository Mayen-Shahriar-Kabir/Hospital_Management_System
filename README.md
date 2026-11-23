# Hospital Management System

A web-based Hospital Management System built with **Python, Django, and
MySQL**. The application provides separate dashboards for
administrators, doctors, and patients to manage hospital operations such
as doctor profiles, appointments, laboratory reports, and payment
requests.

## Features

### Patient

-   Register and log in to a patient account.
-   View the available doctors.
-   Book appointments with doctors.
-   Request laboratory tests.
-   View appointment details, laboratory reports, and payment records.
-   Submit payment requests.

### Doctor

-   Access a dedicated doctor dashboard.
-   View assigned appointments and associated patients.
-   Update appointment statuses.
-   Review laboratory reports and update diagnoses.

### Administrator

-   Access the administrator dashboard.
-   Add doctor accounts and profiles.
-   View payment records and laboratory reports.
-   Update payment statuses.
-   Mark laboratory reports as delivered.

## Technology Stack

-   **Backend:** Python, Django
-   **Database:** MySQL
-   **Frontend:** HTML, CSS, Django Templates
-   **Authentication:** Django Authentication System
-   **ORM:** Django Object-Relational Mapper (ORM)

## Project Structure

``` text
Hospital_Management_System/
├── Hospital/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── hospital_app/
│   ├── migrations/
│   ├── static/
│   │   ├── Images/
│   │   └── css/
│   ├── templates/
│   │   ├── admin_dashboard.html
│   │   ├── doctor_dashboard.html
│   │   ├── patient_dashboard.html
│   │   ├── home.html
│   │   ├── login.html
│   │   └── register.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── signals.py
│   └── admin.py
└── manage.py
```

## Prerequisites

Make sure you have the following installed:

-   Python 3.10 or later
-   MySQL Server
-   pip (Python package manager)

The project uses Django and the MySQL database backend. Install a
compatible Django release and the MySQL Python driver (`mysqlclient`) in
your environment.

## Installation and Setup

### 1. Clone the repository

``` bash
git clone https://github.com/Mayen-Shahriar-Kabir/Hospital_Management_System.git
cd Hospital_Management_System

```

Replace the repository URL with your GitHub repository URL.

### 2. Create and activate a virtual environment

**Windows (PowerShell or CMD):**

``` bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install django mysqlclient
```

If your environment requires additional packages, install them as well.

### 4. Configure MySQL

Start your MySQL server and create a database:

``` sql
CREATE DATABASE hospital;
```

Open `Hospital/settings.py` and configure the `DATABASES` section with
your own MySQL credentials:

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Apply database migrations

Run the following commands from the directory containing `manage.py`:

``` bash
python manage.py makemigrations
python manage.py migrate
```

The repository includes existing migration files, so `makemigrations`
may not be necessary unless you have changed the models.

### 6. Create a Django superuser (optional)

``` bash
python manage.py createsuperuser
```

Follow the prompts to create an account for Django's built-in
administration interface.

### 7. Run the development server

``` bash
python manage.py runserver
```

Open your browser and visit:

``` text
http://127.0.0.1:8000/
```

## Application URLs

  URL                     Purpose
  ----------------------- ----------------------------------------------------
  `/`                     Home page
  `/register/`            Patient registration
  `/login/`               User login
  `/logout/`              User logout
  `/patient/dashboard/`   Patient dashboard
  `/doctor/dashboard/`    Doctor dashboard
  `/admin/dashboard/`     Application administrator dashboard
  `/admin/`               Django built-in admin site (if enabled/configured)

## User Roles

The application defines three user roles:

-   **Admin:** Manages doctor profiles, payment records, and laboratory
    report delivery.
-   **Doctor:** Handles assigned appointments and patient laboratory
    diagnoses.
-   **Patient:** Books appointments, requests laboratory tests, and
    views related records and payments.

## Important Notes

-   This project is configured to use MySQL. Make sure the database
    server is running and the credentials in `Hospital/settings.py` are
    correct.
-   The application should be reviewed and security-tested before being
    used with real patient information or deployed in a production
    healthcare environment.

## Future Improvements

-   Add automated tests for authentication and role-based access.
-   Improve input validation and error handling.
-   Add appointment scheduling and availability validation.
-   Integrate a secure online payment gateway.
-   Improve deployment configuration and application security.
