<h1 align="center">🩺 HealthPal – Digital Healthcare Platform</h1>

<p align="center">
HealthPal is a digital healthcare backend platform designed to support medical and humanitarian services in Palestine.
It streamlines consultations, inventory management, sponsorships, and support services through secure and scalable digital solutions.
</p>


<p align="center">
🚀 <a href="#-demo">View Demo</a> 
</p>

---

<details>
  <summary><strong>📌 Table of Contents</strong></summary>

  <ul>
    <li>🌟 <a href="#-about-the-project">About the Project</a></li>
    <li>🚀 <a href="#-core-features">Core Features</a></li>
    <li>👥 <a href="#-user-roles">User Roles</a></li>
    <li>🛠️ <a href="#-technologies-used">Technologies Used</a></li>
    <li>⚙️ <a href="#-getting-started">Getting Started</a></li>
    <li>📝 <a href="#-api-documentation">API Documentation</a></li>
    <li>📸 <a href="#-demo">Demo</a></li>
    <li>👩‍💻 <a href="#-team">Team</a></li>
  </ul>

</details>


---

## 🌟 About the Project

HealthPal is a digital healthcare backend platform developed to support medical and humanitarian services in Palestine through a secure, scalable, and well-structured system.

The platform enables controlled and transparent interactions between multiple stakeholders, including **patients, doctors, administrators, sponsors, and support organizations**, while ensuring role-based access control and data integrity. HealthPal is designed to streamline core healthcare workflows such as medical consultations, inventory and resource management, sponsorships, and support services.

The system follows **Advanced Software Engineering best practices**, adopting a clean, modular, and layered architecture that promotes maintainability, scalability, and ease of future extension. Each feature is implemented as an independent module, allowing the platform to evolve without impacting existing components.

HealthPal aims to provide a reliable digital healthcare foundation tailored to the Palestinian context, supporting sustainable healthcare operations and improving access to essential medical services through technology.


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

docker compose up --build
```
#### 4️⃣ Apply migrations
```bash

docker compose exec backend python manage.py migrate
```
#### 5️⃣ Create superuser
```bash

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
