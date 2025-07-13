# 📁 File Sharing API

This is a FastAPI-based backend for a simple file sharing service that allows users to sign up, log in, upload files, and download them securely.

---

## 🚀 Features

- ✅ User Sign Up & Login (JWT-based Authentication)
- ✅ Upload Files with Description
- ✅ Download Files via Unique File IDs
- ✅ Password Hashing (bcrypt)
- ✅ PostgreSQL Database Integration
- ✅ Environment Variable Management using .env
- ✅ Tested using Postman

---

## 🧰 Tech Stack

- *FastAPI* - Web framework
- *Uvicorn* - ASGI server
- *PostgreSQL* - Relational database
- *SQLAlchemy* - ORM
- *Passlib[bcrypt]* - Password hashing
- *python-jose* - JWT Token handling
- *dotenv* - Manage environment variables
- *Postman* - API testing

---

## ⚙ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create and Activate Virtual Environment

python -m venv .venv
# For Windows:
.venv\Scripts\activate
# For Mac/Linux:
source .venv/bin/activate

3. Install Requirements

pip install -r requirements.txt

4. Setup .env File

Create a file named .env in the root directory and add your database URL:

DATABASE_URL=postgresql://postgres:sugam7827@localhost:5432/fileshare

Make sure your PostgreSQL server is running and the database fileshare exists.

5. Run the Server

uvicorn app.main:app --reload

Visit: http://127.0.0.1:8000/docs to access Swagger UI and test the API.


---

📮 Postman Collection

A Postman collection is included in the repo for testing:

✅ FileSharing.postman_collection.json

To use:

1. Open Postman


2. Click Import


3. Select the file FileSharing.postman_collection.json


4. Test the API easily with predefined requests


🧑 Author

Made with ❤ by Sugam



