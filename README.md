<h1 align="center">🩺 HealthPal</h1>

<p align="center">
  Digital Healthcare Platform
</p>

<p align="center">
  HealthPal is a backend healthcare platform designed to facilitate medical consultations,
  inventory management, sponsorships, and support services in a secure, organized,
  and transparent digital environment.
</p>

<p align="center">
  👾 <a href="#">View Demo</a> &nbsp;&nbsp; | &nbsp;&nbsp;
  🐞 <a href="#">Report Bug</a>
</p>

---

## 📌 Table of Contents
- [About the Project](#about-the-project)
- [Core Features](#core-features)
- [User Roles](#user-roles)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Demo](#demo)
- [Team](#team)

---

## 🌟 About the Project

HealthPal is a comprehensive backend system built to support healthcare-related services through a modular and scalable architecture.  
The platform connects doctors, patients, sponsors, and administrators while ensuring secure data handling, role-based access control, and efficient service workflows.

The system was designed following layered architecture principles and software engineering best practices, enabling maintainability, scalability, and clear separation of concerns across modules.

---

## 🚀 Core Features

### 🩺 Medical Consultations
- Schedule and manage doctor–patient consultations
- Manage doctor availability slots
- Track consultation history and statuses

### 📦 Inventory Management
- Manage medical items and supplies
- Handle item requests and approvals
- Track inventory availability and usage

### 🤝 Sponsorship & Donations
- Manage sponsorship cases
- Track donations and expense receipts
- Ensure transparency in financial operations

### 👤 User Management
- Secure user authentication and authorization
- Role-based access control using JWT
- Custom user profiles for doctors and administrators

### 🔐 Security & Access Control
- JWT-based authentication
- Permission-based API access
- Secure handling of sensitive data

---

## 👥 User Roles

- 👨‍⚕️ **Doctor**: Manage availability and consultations  
- 🧑‍⚕️ **Patient**: Request and attend consultations  
- 🎗️ **Sponsor**: Support medical and humanitarian cases  
- 🧾 **Administrator**: Manage users, inventory, sponsorships, and system data  

---

## 🔨 Technologies Used

- **Django** – Backend web framework  
- **Django REST Framework** – RESTful API development  
- **JWT (SimpleJWT)** – Authentication and authorization  
- **MySQL** – Relational database  
- **Docker & Docker Compose** – Containerized development environment  
- **Postman** – API testing and documentation  
- **GitHub** – Version control and collaboration  

---

## ⚙️ Getting Started

### 🧩 Prerequisites
Make sure you have the following installed:
- Docker
- Docker Compose
- Git

### 🚀 Running the Project

1. Clone the repository:
```bash
git clone https://github.com/your-username/healthpal.git
cd healthpal
Create an .env file in the project root and configure environment variables:

env
Copy code
DEBUG=True
SECRET_KEY=your_secret_key

DB_NAME=healthpal_db
DB_USER=healthpal_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=3306
Build and run the containers:

bash
Copy code
docker compose up --build
Apply migrations:

bash
Copy code
docker compose exec backend python manage.py migrate
Create a superuser:

bash
Copy code
docker compose exec backend python manage.py createsuperuser
Access the application:

Admin Panel: http://localhost:8000/admin

API Base URL: http://localhost:8000/api

📝 API Documentation
Our API is fully documented and accessible through Postman, providing a detailed guide for all endpoints.
You can view the latest API documentation here once the backend is live.

The documentation includes:

Endpoint descriptions

Request parameters

Response formats

Practical usage examples

📸 Demo
Get a firsthand look at HealthPal in action!
🚀 View Demo

👩‍💻 Team
Dana sharaqa
Tala Alhendi
Mustafa Ahmad

[Add other team members here]

<p align="center"> Built with ❤️ for Advanced Software Engineering </p> ```
