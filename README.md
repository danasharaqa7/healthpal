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

The platform enables controlled and transparent interactions between multiple stakeholders, including **patients, doctors, administrators, sponsors, NGOs, and support organizations**, while enforcing **Role-Based Access Control (RBAC)** and ensuring data integrity.

HealthPal focuses on streamlining essential healthcare workflows such as medical consultations, inventory and resource management, sponsorships, and humanitarian support services.

The system follows **Advanced Software Engineering best practices**, adopting a clean, modular, and layered architecture that improves maintainability, scalability, and ease of future extension. Each feature is implemented as an independent module, allowing the platform to evolve without impacting existing components.

---

## 🚀 Core Features

🩺 **Medical Consultations**
- Schedule and manage doctor consultations  
- Define doctor availability slots  
- Maintain secure consultation records  

📦 **Medical Inventory Management**
- Track medical items and stock levels  
- Manage inventory requests  
- Control stock availability  

🤝 **Sponsorship & Donations**
- Manage sponsorship cases  
- Track donations and expense receipts  
- Ensure transparency in financial workflows  

🆘 **Support Services**
- Handle humanitarian and support requests  
- Apply role-based permissions for service management  

🔐 **Authentication & Security**
- JWT-based authentication  
- Role-based authorization (RBAC)  
- Secure API access  

---

## 👥 User Roles

HealthPal adopts a **Role-Based Access Control (RBAC)** model, where logical role separation is enforced at the application level to ensure clarity, security, and controlled user interactions.

👤 **Patient**
- Requests medical consultations  
- Submits medical inventory requests  
- Accesses humanitarian and support services  

👨‍⚕️ **Doctor**
- Manages availability slots  
- Conducts medical consultations  
- Can be local or international  
- Requires admin verification  

🎗 **Sponsor / Donor**
- Supports medical cases financially  
- Tracks donations and expense receipts  

🏥 **NGO Staff**
- Manages medical inventory and resources  
- Reviews and fulfills item requests  
- Oversees sponsorship cases  

🆘 **Support Agent**
- Handles humanitarian and support service requests  
- Provides assistance for sensitive cases  

🔧 **Admin**
- Full system access  
- Manages users and roles  
- Verifies doctors and NGOs  
- Oversees platform operations  

---

## 🛠 Technologies Used

- **Python & Django** – Backend framework  
- **Django REST Framework (DRF)** – RESTful API development  
- **MySQL** – Relational database  
- **Docker & Docker Compose** – Containerization and environment consistency  
- **JWT Authentication** – Secure access control  
- **Swagger & ReDoc (drf-spectacular)** – API documentation  
- **Git & GitHub** – Version control and collaboration  

---

## ⚙️ Getting Started

### 🚀 Running the Project

#### 1️⃣ Clone the repository
```bash
git clone https://github.com/danasharaqa7/healthpal.git
cd healthpal
```

#### 2️⃣ Create `.env` file
Create a `.env` file in the project root directory and add the following environment variables:

```env
DEBUG=True
SECRET_KEY=your_secret_key

DB_NAME=healthpal_db
DB_USER=healthpal_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=3306
```

#### 3️⃣ Build & run Docker containers
```bash
docker compose up --build
```

#### 4️⃣ Apply database migrations
```bash
docker compose exec backend python manage.py migrate
```

#### 5️⃣ Create a superuser (Admin account)
```bash
docker compose exec backend python manage.py createsuperuser
```

Follow the prompts to set the admin email and password.

#### 6️⃣ Access the application
```
Admin Panel: http://localhost:8001/admin
API Base URL: http://localhost:8001/api
```
---

## 📝 API Documentation

The HealthPal API is fully documented to support both development and presentation needs.

- **Swagger UI** is used for interactive API testing during development.
- **ReDoc** provides a clean and professional API documentation view for reference and review.

### 📌 Available Documentation
- Swagger UI: http://localhost:8001/api/schema/swagger-ui/
- ReDoc: http://localhost:8001/api/schema/redoc/

The documentation includes:
- Endpoint descriptions  
- Request parameters  
- Response formats  
- Authentication requirements  

---

## 📸 Demo

Get a firsthand look at **HealthPal** in action 🚀  
👉 **View Demo:**  
[Watch the demo video](https://drive.google.com/drive/folders/18fRbzJmQLBays6ecs-vQwiIg_OGVRoZ1?usp=sharing)


## 👩‍💻 Team

- **Dana Sharaqa**  
  📧 [danasharaqan1@gmail.com](mailto:danasharaqan1@gmail.com)

- **Tala Alhendi**  
  📧 [talaalhendiuni4@gmail.com](mailto:talaalhendiuni4@gmail.com)

- **Mustafa Ahmad**  
  📧 [3tnawi.3tm@gmail.com](mailto:3tnawi.3tm@gmail.com)
