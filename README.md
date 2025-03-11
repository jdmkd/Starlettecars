# Project Setup Guide

Welcome to the project! This guide will help you set up and run the project efficiently.

---
## 🚀 Getting Started

### Open the project in VS Code or your favorite editor.

---
## 🐍 Python3 & Django 5.0.6 Setup

### 1️⃣ Prerequisites:
Ensure you have the following installed:
- **Python 3.12.0**
- **pip 24.3.1** (Python package manager)

### 2️⃣ Install Virtual Environment:
If you don't have `virtualenv` installed, run:
```sh
pip install virtualenv
```

### 3️⃣ Create a Virtual Environment:
Navigate to your project's root directory (where `manage.py` is located) and run:
```sh
virtualenv venv
```
This will create a `.venv` folder at your project's root.

### 4️⃣ Activate the Virtual Environment:
For Windows:
```sh
venv\Scripts\activate
```
Once activated, you'll see `(venv)` at the beginning of your terminal prompt.

### 5️⃣ Install Dependencies:
Run the following command to install all required libraries:
```sh
pip install -r requirements.txt
```
Now, all necessary dependencies are installed.

---
## 🛠 Database Setup
This project supports **PostgreSQL** and **SQLite**.

### 🔹 Option 1: PostgreSQL Setup (Recommended)
If using PostgreSQL, create a `.env` file at the project root and add the following configurations:
```env
# Database Configuration
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```
⚠️ **No need to modify** `DATABASES` in `settings.py`. The project will automatically detect these values.

### 🔹 Option 2: SQLite Setup (Default)
If you prefer SQLite, update `settings.py` as follows:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
```

---
## 🔄 Applying Migrations
Run the following commands to set up the database schema:
```sh
python manage.py makemigrations
python manage.py migrate
```

---
## 👤 Create a Superuser
To create an admin account, run:
```sh
python manage.py createsuperuser
```
Follow the prompts to set up your admin credentials.

---
## 🚀 Run the Development Server
Start your Django project with:
```sh
python manage.py runserver
```
Your project is now running! 🎉

---
## 🎨 Tailwind CSS Setup
This project uses **Tailwind CSS** for styling.

### 1️⃣ Initialize Node.js Setup:
Open a separate terminal (not inside the virtual environment) and run:
```sh
npm init -y
```

### 2️⃣ Install Tailwind CSS:
```sh
npm install -D tailwindcss
npx tailwindcss init
```

### 3️⃣ Start the Tailwind Build Process:
```sh
npm run tailwind-build
npm run tailwind-watch
```

### 4️⃣ Serve Tailwind CSS:
Navigate to the `tailwindrun` folder and run:
```sh
cd tailwindrun
npm run dev
```
This serves the `tailwind-output.css` file.

### 5️⃣ Link Tailwind in HTML:
Add the following line inside the `<head>` tag of your HTML files:
```html
<link href="{% static 'css/tailwind-output.css' %}" rel="stylesheet" />
```

---
## 🎯 Done!
Your project is now fully set up and ready to go! 🚀

Thanks for using this guide. Happy coding! 😊

