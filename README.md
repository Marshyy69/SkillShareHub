# ⚡ SkillShare Hub

SkillShare Hub is a localized, peer-to-peer freelance and micro-task marketplace website designed for students and local communities. Users can register as **Buyers** to purchase services or **Sellers** to list services (gigs), accept orders, and deliver completed work.

---

## 📂 What to zip (and what to exclude)
When sharing this project folder, make sure to **exclude** the following to keep the zip file size small:
* ❌ `.venv/` (your local virtual environment - they will create their own)
* ❌ `.idea/` (PyCharm configuration files)
* ❌ `__pycache__/` folders (Python execution cache)

**Keep everything else**, including:
* `marketplace/` (app code)
* `skillshare_hub/` (project configurations)
* `static/` (CSS styling)
* `media/` (uploaded images/files - optional, keep if you want to share test images)
* `requirements.txt` (dependencies list)
* `db.sqlite3` (database - keep this if you want to share registered test accounts and gigs, or delete/exclude it if you want them to start with a fresh blank database)
* `manage.py`

---

## 🚀 Setup Instructions for Your Friends

Follow these steps to set up and run the project on your machine:

### 1. Prerequisites
Make sure you have **Python 3.10+** installed on your system.

### 2. Extract the Folder
Unzip the project files into a folder on your computer.

### 3. Open Terminal / Command Prompt
Open your terminal (PowerShell, Command Prompt, or Bash) and navigate to the project directory:
```bash
cd path/to/SkillShareHub
```

### 4. Create a Virtual Environment
Run the following command to create a virtual environment named `.venv`:
* **Windows (PowerShell / CMD):**
  ```powershell
  python -m venv .venv
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  ```

### 5. Activate the Virtual Environment
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

### 6. Install Dependencies
Install Django and Pillow (used for image handling) using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 7. Run Database Migrations (If starting fresh)
If you deleted `db.sqlite3` to start with a fresh database, run migrations to set up the database tables:
```bash
python manage.py migrate
```
*(If you kept `db.sqlite3`, you can skip this step!)*

### 8. Create an Admin Account (Optional)
Create a superuser account to access the Django admin dashboard (`/admin/`):
```bash
python manage.py createsuperuser
```

### 9. Start the Server!
Launch the development server:
```bash
python manage.py runserver
```

Now open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser to explore SkillShare Hub! 🚀
