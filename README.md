## Features
- Search for flights using their flight ID.
- View detailed flight information, including aircraft details and images.
- Get information about airports, including their ICAO code.
- Chatbot added.

---

## Prerequisites
To run this project, ensure you have the following installed:

1. Python 3.8 or higher
2. pip (Python package installer)
3. Git

---

## Installation Steps

### Step 1: Clone the Repository

### Step 2: Set Up a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # For macOS/Linux
# On Windows:
# .venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations
```bash
python manage.py migrate
```

### Step 5: Run the Development Server
```bash
python manage.py runserver
```

### Step 6: Access the Application
Open your browser and go to:
```
http://127.0.0.1:8000/
```

---

## API Key Setup
This project uses the Aerodatabox API to fetch flight and airport data. Ensure you have a valid API key.

1. Replace the API key in `views.py` with your own:
   ```python
   headers = {'x-magicapi-key': 'YOUR_API_KEY'}
   ```
2. Save the file.

---

## Collaboration Workflow
If you're working on this project with friends:

1. Clone the repository (as shown above).
2. Make your changes locally.
3. Add and commit your changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   ```
4. Push your changes:
   ```bash
   git push origin main
   ```
5. If there are conflicts, resolve them locally and push again.

---

## Troubleshooting
- If you encounter "ModuleNotFoundError", ensure all dependencies are installed using:
  ```bash
  pip install -r requirements.txt
  ```

- If migrations fail, ensure your database setup is correct and retry:
  ```bash
  python manage.py migrate
  ```

---

## Contributors
- Caner Akçasu (SD1)
- Kaan Yazicioglu (SD4)

---

## License
This project is open-source and available under the [MIT License](LICENSE).

