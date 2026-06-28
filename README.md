# ⚡ SkillShare Hub

SkillShare Hub is a localized, peer-to-peer freelance and micro-task marketplace website designed for students and local communities. Users can register as **Buyers** to purchase services or **Sellers** to list services (gigs), accept orders, and deliver completed work.

---

## 🚀 Setup Instructions

Follow these steps to set up and run the project locally on your machine:

### 1. Prerequisites
Make sure you have **Python 3.10+** and **Git** installed on your system.

### 2. Clone the Repository
Open your terminal (PowerShell, Command Prompt, or Bash) and run:
```bash
git clone <github-repository-url>
cd SkillShareHub
```
*(Replace `<github-repository-url>` with the URL of your repository on GitHub)*

### 3. Create a Virtual Environment
Run the following command to create a virtual environment named `.venv`:
* **Windows (PowerShell / CMD):**
  ```powershell
  python -m venv .venv
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  ```

### 4. Activate the Virtual Environment
Activate the environment:
* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 5. Install Dependencies
Install Django and Pillow (used for image handling) using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 6. Run Database Migrations
Run the migrations to set up your local database tables:
```bash
python manage.py migrate
```

### 7. Create an Admin Account (Optional)
Create a superuser account to access the Django admin dashboard (`/admin/`):
```bash
python manage.py createsuperuser
```

### 8. Start the Server!
Launch the development server:
```bash
python manage.py runserver
```

Now open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser to explore SkillShare Hub! 🚀
