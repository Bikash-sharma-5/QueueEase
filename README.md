# QueueEase - Smart Queue Management System
![Screenshot 2025-03-26 013315](https://github.com/user-attachments/assets/4f8a7ac4-20b7-4474-a1ad-f80cedef01af)
![Screenshot 2025-03-26 013402](https://github.com/user-attachments/assets/7283ad73-e8ee-4704-b73e-73973a641ee4)

QueueEase is a web-based queue management system that allows users to join queues digitally, receive real-time position updates, and minimize waiting times. Businesses can efficiently manage queues, reducing congestion and improving customer experience.

## 🚀 Features

✅ **QR Code-Based Queue Joining** - Users scan a QR code to enter the queue.
✅ **Real-Time Position Updates** - Receive live notifications via SMS & Email.
✅ **Admin Dashboard** - Monitor and manage queues efficiently.
✅ **Dynamic Queue Positioning** - Automatic movement as users are served.
✅ **Multi-Channel Notifications** - Stay informed through email & SMS.
✅ **Secure Authentication** - User login & role-based access.
✅ **Analytics & Reporting** - Gain insights on queue performance.

---

## 📂 Project Structure

```
QueueEase/
│── queueapp/          # Main application
│   ├── migrations/    # Database migrations
│   ├── templates/     # HTML templates
│   ├── static/        # CSS, JS, images
│   ├── views.py       # Application logic
│   ├── models.py      # Database models
│   ├── urls.py        # URL routing
│   ├── forms.py       # Forms handling
│── queueease/         # Project configuration
│── db.sqlite3         # SQLite database (for development)
│── manage.py          # Django CLI
│── requirements.txt   # Dependencies
```

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/queueease.git
cd queueease
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 5️⃣ Create a Superuser (for Admin Access)
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Development Server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** to access the application.

---

## 🔗 API Endpoints

| Endpoint         | Method | Description                      |
|-----------------|--------|----------------------------------|
| `/register/`    | POST   | User Registration               |
| `/login/`       | POST   | User Authentication             |
| `/queue/join/`  | POST   | Join a queue                    |
| `/queue/status/`| GET    | Check queue position            |
| `/queue/leave/` | POST   | Leave a queue                   |

---


## 📜 License
This project is licensed under the MIT License.

---

## 🤝 Contributing
Pull requests are welcome! Open an issue for feature suggestions.

---

## 📧 Contact
For inquiries, reach out at **bikashsharma5151@gmail.com**

---

### 🎉 Happy Queue Management!

