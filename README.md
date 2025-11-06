# Albonyan AlMarsous 

## 🌍 About the Project

**Albonyan AlMarsous** is a web application that helps patients share their stories and receive emotional and financial support from others.  
Patients can write posts, create donation campaigns, and communicate with supporters.  
Supporters can view patient posts, leave comments and likes, and donate securely.

This project was built using **React (Vite)** for the frontend and **Django REST Framework** for the backend.

---

## ⚛️ Frontend Tech Stack

### 🖥️ Frontend
- React (Vite)
- JavaScript 
- React Router DOM
- Axios 
- Bootstrap
- Custom CSS 

### ⚙️ Backend
- Django REST Framework
- Python
- PostgreSQL
- JWT Authentication

### 🧰 Dev Tools
- Git & GitHub
- Docker
- Postman

---

## 🔗 Links

- **Backend Repository:** [Albonyan AlMarsous Frontend](https://github.com/alhassan-alshareef/albonyan-almarsous-frontend)

---


## 🗺️ Entity Relationship Diagram (ERD)

The diagram below shows the main models and the relationships between them in the project.

![ERD Diagram](./Erd-diagram.png)

---

## General Routes

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **POST** | `/api/contact/` | Send a contact message to the admin email |




## 🔐 Auth & User Routes

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **POST** | `/api/signup/` | Register a new account (either patient or supporter) |
| **POST** | `/api/login/` | Log in and receive a JWT token |
| **GET** | `/api/profile/` | Get logged-in user profile information |
| **PUT** | `/api/profile/` | Update logged-in user profile |

---

## Post Routes

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **GET** | `/api/patient/posts/` | Get all patient posts |
| **POST** | `/apipatient/posts/` | Create a new post (only if role = patient) |
| **GET** | `/apipatient/posts/:id/` | View a single post by ID |
| **PUT** | `/api/patient/posts/:id/` | Edit a post (only if role = patient) |
| **DELETE** | `/api/patient/posts/:id/` | Delete a post (only if role = patient) |

---

## 💬 Comment Routes

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **GET** | `/api/posts/:post_id/comments/` | Get all comments for a specific post |
| **POST** | `/api/posts/:post_id/comments/` | Add a comment (supporter only) |
| **PUT** | `/api/comments/:id/` | Edit a comment (only the owner can edit) |
| **DELETE** | `/api/comments/:id/` | Delete a comment (only the owner can delete) |

---

## ❤️ Like Routes

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **POST** | `/api/posts/:id/like/` | Like or unlike a post (supporter only) |

---

## 💰 Donation Routes

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **GET** | `/api/donations/` | View all active donation campaigns |
| **POST** | `/api/patient/donations/` | Create a new donation campaign (patient only) |
| **GET** | `/api/patient/donations/:id/` | View a single donation campaign (patient only) |
| **PUT** | `/api/patient/donations/:id/` | Update donation goal or title (patient only) |
| **DELETE** | `/api/patient/donations/:id/` | Delete a donation campaign (patient only) |
| **POST** | `/api/donations/:id/pay/` | Make a donation for a patient (supporter only) |

---

## 🔗 Links

- **Backend Repository:** [Albonyan AlMarsous Backend](https://github.com/alhassan-alshareef/albonyan-almarsous-backend)

---
## Installation Instructions (Docker)

### 1️⃣ Clone both repositories inside the same parent folder
```bash
parent-folder/
├── Albonyan-AlMarsous-backend/
└── Albonyan-AlMarsous-frontend/
```

### 2️⃣ Clone the backend repository
```bash
git clone https://github.com/YourUsername/Albonyan-AlMarsous-backend.git

```

### 3️⃣ Clone the frontend repository
```bash
git clone https://github.com/YourUsername/Albonyan-AlMarsous-frontend.git

```
### 4️⃣ Run Docker Compose from the backend folder
```bash
cd Albonyan-AlMarsous-backend
docker compose up --build
```

## 📘 What I Learned

- How to connect **React** with **Django REST APIs**  
- How **JWT authentication** works for securing user access  
- How to use **Docker** to run full-stack web applications  
- How to design **clean, reusable React components**  
- How to test and debug APIs using **Postman**

---
## 🧊 Future Ideas

- Add a Patient Appointments Page to show available visiting times.
- Add a Donation Shop Page where patients (or their families) can sell items they no longer need.
- Add Multi-language support (English + Arabic).
- Add an Admin Dashboard 

---
## 👨‍💻 Author

**Alhassan Ali Alshareef**  
Saudi Digital Academy – Software Engineering Bootcamp  


🌐 [GitHub Profile](https://github.com/alhassan-alshareef)

