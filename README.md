# E‑Academy 🎓

E‑Academy is a **full‑stack e‑learning platform** built with **Django**, designed to manage online courses, educational content, and user authentication within a modular and production‑ready architecture. The project follows standard Django best practices and is structured for deployment.

---

## ✨ Features

* Modular Django project structure (apps‑based design)
* User authentication and account management
* Course and educational content management
* Blog / content section for articles and announcements
* Static files handling for production
* SQLite database (easily replaceable for production)

---

## 🛠 Tech Stack

* **Backend:** Django (Python)
* **Database:** SQLite (development / default)
* **Frontend:** Django Templates + Static Files
* **Environment Management:** Pipenv
* **Deployment:** Gunicorn + Procfile support

---

## 📂 Project Structure

```text
e_academy/
│
├── academy/              # Core project configuration
├── accounts/             # User authentication & profiles
├── academy_courses/      # Courses and educational content
├── academy_blog/         # Blog and articles module
├── staticfiles/          # Collected static files (deployment)
│
├── manage.py             # Django management entry point
├── db.sqlite3            # Database (replaceable in production)
├── requirements.txt      # Production dependencies
├── Pipfile / Pipfile.lock
├── Procfile              # Deployment entry point
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/HamzaWaleedDV/e_academy.git
cd e_academy
```

### 2️⃣ Create virtual environment & install dependencies

Using Pipenv:

```bash
pipenv install
pipenv shell
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Apply migrations

```bash
python manage.py migrate
```

---

### 4️⃣ Run the development server

```bash
python manage.py runserver
```

Access the application at:

```
http://127.0.0.1:8000/
```

---

## 🧠 Design Principles

* Clear separation of concerns via Django apps
* Maintainable and scalable architecture
* Production‑aware configuration
* Built as a real‑world educational platform, not a demo

---

## 👤 Author

**Hamza Waleed**

---

## 📄 License

This project is provided for educational and portfolio purposes.
