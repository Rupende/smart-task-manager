# 🚀 Smart Task Manager

A modern, full-stack **Task Management Web Application** built with **Python (Flask)**.
This project demonstrates real-world development practices including authentication, CRUD operations, database design, and data visualization — making it ideal for a developer portfolio.

---

## 📌 Overview

Smart Task Manager is designed to help users efficiently manage their daily tasks with a clean and intuitive interface. It combines backend logic with a user-friendly frontend to deliver a seamless productivity experience.

---

## ✨ Features

### 🔐 Authentication

* Secure user registration and login
* Password hashing for security
* Session-based authentication
* Protected routes for authorized access

### 👤 User Management

* Unique username enforcement
* Secure login/logout functionality
* Persistent user sessions

### ✅ Task Management

* Create, update, and delete tasks
* Assign priority levels (Low, Medium, High)
* Track task status (Pending / Completed)
* Personalized tasks per user

### 🔍 Search & Filtering

* Search tasks by keywords
* Filter tasks by priority or status
* Organized task display

### 📊 Analytics Dashboard

* Total tasks overview
* Completed vs pending tasks
* Visual insights using charts (e.g., pie chart)

### 🖥️ User Dashboard

* Task creation form
* Task table view
* Status updates
* Task deletion
* Integrated analytics


---

## 🗄️ Database Schema

### Users Table

| Field    | Type    | Description     |
| -------- | ------- | --------------- |
| id       | Integer | Primary Key     |
| username | Text    | Unique Username |
| password | Text    | Hashed Password |

### Tasks Table

| Field      | Type     | Description         |
| ---------- | -------- | ------------------- |
| id         | Integer  | Primary Key         |
| user_id    | Integer  | Foreign Key (Users) |
| title      | Text     | Task Title          |
| priority   | Text     | Low / Medium / High |
| status     | Text     | Pending / Completed |
| created_at | DateTime | Timestamp           |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Rupende/smart-task-manager.git
cd smart-task-manager
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask
```

### 5. Run the Application

```bash
python app.py
```

### 6. Open in Browser

```
http://127.0.0.1:5000
```

---

## 🧠 Technologies Used

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, Jinja2
* **Database:** SQLite
* **Authentication:** Session-based + Password Hashing

---

## 🎯 Learning Outcomes

This project demonstrates:

* Full-stack web development with Flask
* Secure authentication systems
* Database design and relationships
* CRUD operations
* Search and filtering logic
* Data visualization
* Clean UI/UX design

---

## 💡 Future Improvements

* AJAX for real-time updates
* Dark mode support 🌙
* Flask Blueprints for scalability
* Form validation & flash messages
* REST API integration
* Deployment (Render, Railway, or Heroku)


---

## 🚀 Deployment

You can deploy this app using:

* Render
* Railway
* Heroku

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

## 👨‍💻 Author

**Munashe Rupende**

* GitHub: [https://github.com/Rupende](https://github.com/Rupende)
