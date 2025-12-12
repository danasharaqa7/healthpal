<h1 align="center">🩺 HealthPal – Digital Healthcare Platform</h1>

<p align="center">
<strong>HealthPal</strong> is a digital healthcare backend platform designed to support and strengthen healthcare services in Palestine, especially in environments facing limited resources and system disruptions.  
The platform provides a unified and secure digital infrastructure for medical consultations, treatment sponsorships, medication coordination, and community health support.
<br/><br/>
HealthPal connects patients, doctors, donors, NGOs, and healthcare administrators through scalable APIs, enabling transparent service workflows, efficient resource management, and improved access to essential medical care.  
Built with a focus on reliability, modularity, and security, the system aims to leverage technology to enhance healthcare accessibility and resilience within the Palestinian context.
</p>


<p align="center">
🚀 <a href="#-demo">View Demo</a> 
</p>

---

## 📌 Table of Contents
- [🌟 About the Project](#-about-the-project)
- [🚀 Core Features](#-core-features)
- [👥 User Roles](#-user-roles)
- [🛠 Technologies Used](#-technologies-used)
- [⚙️ Getting Started](#️-getting-started)
- [📝 API Documentation](#-api-documentation)
- [📸 Demo](#-demo)
- [👩‍💻 Team](#-team)

---

## 🌟 About the Project
HealthPal is a backend healthcare platform built to support medical and humanitarian services through a clean, layered architecture.  
It enables secure interactions between doctors, patients, sponsors, and administrators while ensuring transparency, role-based access control, and efficient service workflows.

The system follows **best practices in Advanced Software Engineering**, emphasizing modularity, scalability, and maintainability.

---

## 🚀 Core Features
🩺 **Medical Consultations**  
- Schedule and manage doctor consultations  
- Doctor availability slots  
- Secure consultation records  

📦 **Medical Inventory Management**  
- Track medical items  
- Manage inventory requests  
- Control stock availability  

🤝 **Sponsorship & Donations**  
- Manage sponsorship cases  
- Track donations and expense receipts  
- Transparent financial workflows  

🆘 **Support Services**  
- Handle support requests  
- Role-based permissions for service management  

🔐 **Authentication & Security**  
- JWT-based authentication  
- Role-based authorization  
- Secure API access  

---

## 👥 User Roles
👤 **Patient** – Requests consultations and support services  
👨‍⚕️ **Doctor** – Manages availability and consultations  
🎗 **Sponsor** – Supports cases financially  
🔧 **Admin** – Oversees users, services, and platform data  

---

## 🛠 Technologies Used
- **Python & Django** – Backend framework  
- **Django REST Framework (DRF)** – API development  
- **MySQL** – Relational database  
- **Docker & Docker Compose** – Containerization  
- **JWT Authentication** – Secure access  
- **Swagger (drf-spectacular)** – API documentation  
- **Git & GitHub** – Version control and collaboration  

---

## ⚙️ Getting Started

### 🚀 Running the Project

#### 1️⃣ Clone the repository
```bash
git clone https://github.com/danasharaqa7/healthpal.git
cd healthpal
```
#### 2️⃣ Create .env file
Create a .env file in the project root:
```bash
env
Copy code
DEBUG=True
SECRET_KEY=your_secret_key

DB_NAME=healthpal_db
DB_USER=healthpal_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=3306
```
#### 3️⃣ Build & run containers

```bash
Copy code
docker compose up --build
```
#### 4️⃣ Apply migrations
```bash
Copy code
docker compose exec backend python manage.py migrate
```
#### 5️⃣ Create superuser
```bash
Copy code
docker compose exec backend python manage.py createsuperuser
```
#### 6️⃣ Access the application
```
Admin Panel: http://localhost:8001/admin

API Base URL: http://localhost:8001/api
```

## 📝 API Documentation

Our API is fully documented using **Swagger**, providing an interactive and clear overview of all available endpoints.

Once the backend is running, you can access the documentation here:  
👉 **Swagger UI:** [http://localhost:8001/api/schema/swagger-ui/](http://localhost:8001/api/schema/swagger-ui/)

The documentation includes:
- Endpoint descriptions  
- Request parameters  
- Response formats  
- Practical usage examples  

## 📸 Demo

Get a firsthand look at **HealthPal** in action 🚀  
👉 **View Demo:**  
[Watch the demo video](https://drive.google.com/drive/folders/18fRbzJmQLBays6ecs-vQwiIg_OGVRoZ1?usp=sharing)

## 👩‍💻 Team

- **Dana Sharaqa**  
  📧 [danasharaqan1@gmail.com](mailto:danasharaqan1@gmail.com)

- **Tala Alhendi**  
  📧 [talaalhendiuni4@gmail.com.com](mailto:talaalhendiuni4@gmail.com)

- **Mustafa Ahmad**  
  📧 [3tnawi.3tm@gmail.com](mailto:3tnawi.3tm@gmail.com)
