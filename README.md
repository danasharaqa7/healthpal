🩺 HealthPal – Digital Healthcare Platform

HealthPal is a backend healthcare platform designed to facilitate medical consultations, inventory management, sponsorships, and support services in an organized and transparent way.
The system aims to improve accessibility to healthcare resources through digital solutions, enabling efficient management of users, medical services, and donations.

📌 Table of Contents

About the Project

Core Features

User Roles

Technologies Used

Getting Started

API Documentation

Demo

Team

🌟 About the Project

HealthPal is a comprehensive backend system built to support healthcare-related services through a modular and scalable architecture.
The platform connects doctors, patients, sponsors, and administrators while ensuring secure data handling, role-based access, and efficient service workflows.

The system was designed following layered architecture principles and best practices in software engineering, focusing on maintainability, scalability, and clarity of responsibilities.

🚀 Core Features
🩺 Medical Consultations

Manage online consultations between patients and doctors

Doctor availability slots and scheduling

Consultation status tracking

📦 Inventory Management

Manage medical items and supplies

Track inventory availability

Handle item requests efficiently

🤝 Sponsorships & Donations

Manage sponsorship cases

Track donations and expense receipts

Ensure transparency and accountability

👤 User Management

Custom user model

Role-based access control

Secure authentication system

🛡️ Security & Architecture

JWT-based authentication

Modular Django apps

Environment-based configuration using .env

👥 User Roles

👨‍⚕️ Doctor – Provides medical consultations

👤 Patient – Requests consultations and services

🤝 Sponsor – Supports medical cases and donations

🛠️ Admin – Manages the platform and oversees operations

🔨 Technologies Used

Python – Core programming language

Django – Backend web framework

Django REST Framework (DRF) – API development

MySQL – Relational database

Docker & Docker Compose – Containerization

JWT (SimpleJWT) – Authentication

Postman – API testing & documentation

GitHub – Version control and collaboration

⚙️ Getting Started
🔹 Prerequisites

Make sure you have installed:

Python 3.10+

Docker & Docker Compose

Git

🔹 Running the Project (Docker)

1️⃣ Clone the repository:

git clone https://github.com/danasharaqa7/healthpal.git
cd healthpal


2️⃣ Create a .env file in the root directory:

DEBUG=True
SECRET_KEY=your_secret_key

DB_NAME=healthpal_db
DB_USER=healthpal_user
DB_PASSWORD=healthpal_password
DB_HOST=db
DB_PORT=3306


3️⃣ Run the project:

docker compose up --build


4️⃣ Apply migrations:

docker compose exec backend python manage.py migrate


5️⃣ Create superuser:

docker compose exec backend python manage.py createsuperuser


6️⃣ Access the admin panel:

http://localhost:8000/admin

📝 API Documentation

Our API is fully documented and accessible through Postman, providing a detailed guide for all endpoints.
You can view the latest API documentation here
 once the backend is live.

The documentation includes:

Endpoint descriptions

Request parameters

Response formats

Example requests

📸 Demo

Get a firsthand look at HealthPal in action!
🚀 View Demo

👩‍💻 Team

Dana

Tala

(Add remaining team members if needed)

✨ HealthPal was developed as part of an Advanced Software Engineering project, applying modern backend development practices and collaborative workflows.
