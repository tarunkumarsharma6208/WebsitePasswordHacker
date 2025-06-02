# 🔐 Website Password Hacker (Django Project)

This Django project simulates a website password hacking interface for educational and ethical testing purposes. 
It is designed to help security enthusiasts, students, and developers understand how password brute-force or vulnerability testing can work, within legal and controlled environments.

## 🚀 Features

- Simulated password input and brute-force interface
- Django-based web application
- Educational user flow to demonstrate how attacks may be structured
- Customizable configurations for target simulation

> ⚠️ **This project does NOT hack real websites. It simulates the experience in a controlled, local environment.**

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/tarunkumarsharma6208/WebsitePasswordHacker.git
cd website-password-hacker

# Create virtual environment and install dependencies
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Run Django server
python manage.py migrate
python manage.py runserver
