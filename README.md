# 🔌 ElectroMart — Online Electronics Store with M-Pesa Payments

ElectroMart is a modern e-commerce web application for selling electronic products online. It allows users to browse a wide range of electronics, add items to their cart, and pay securely using M-Pesa.

---

## 🚀 Features

- 🛒 Add to Cart functionality
- 👤 User registration and login
- 💳 M-Pesa integration for secure payments
- 📱 Responsive design (mobile-friendly)

---

## 💻 Tech Stack

- **Frontend**: HTML, CSS, JavaScript 
- **Backend**: Django 
- **Database**: PostgreSQL
- **Payments**: M-Pesa Daraja API (Safaricom)
- **Authentication**: session-based login

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/GERRY-01/Electronics-Ecommerce-app
   ```

## 2 Install dependancies 

```bash
    pip install -r requirements.txt

```
### 3 Set up environment variables
Create a .env file with your credentials:

# Email SMTP Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password

# M-Pesa Daraja API (Sandbox or Production)
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_PASSKEY=your_mpesa_passkey
MPESA_API_URL=https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials
LIPA_NA_MPESA_URL=https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest
MPESA_SHORTCODE=your_shortcode

# PostgreSQL Database Settings
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

## 4. Run database migrations

```bash
python manage.py migrate
```

## 5. Start the development server

```bash
python manage.py runserver
```