/* search_results.css */
body {
    background: var(--background);
    color: var(--text);
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

.header-container {
    background: var(--primary);
    color: var(--text);
    padding: 20px;
    text-align: center;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background: var(--card-bg);
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.flight-card {
    background: var(--card-bg);
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.flight-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--text-light);
    padding-bottom: 10px;
    margin-bottom: 10px;
}

.flight-header h2 {
    margin: 0;
}

.flight-header .status {
    font-size: 1.2rem;
    color: var(--secondary);
}

.flight-info {
    display: flex;
    justify-content: space-between;
}

.flight-info div {
    width: 45%;
}

.flight-info h3 {
    margin-top: 0;
}

.back-button {
    display: inline-block;
    padding: 10px 20px;
    background: var(--primary);
    color: var(--text);
    text-decoration: none;
    border-radius: 5px;
    text-align: center;
}

.back-button:hover {
    background: var(--secondary);
}

.completion-bar-container {
    text-align: center;
    margin-top: 20px;
}

.completion-bar-container progress {
    width: 100%;
    height: 20px;
    border-radius: 10px;
    overflow: hidden;
}

.completion-bar-container label {
    display: block;
    margin-bottom: 10px;
}# Airport Tracker Project

This project is a Django-based web application that allows users to track flights and gather information about airports. The application fetches data from the Aerodatabox API to provide detailed flight and airport information.

---

## Features
- Search for flights using their flight ID.
- View detailed flight information, including aircraft details and images.
- Get information about airports, including their ICAO code.

---

## Prerequisites
To run this project, ensure you have the following installed:

1. Python 3.8 or higher
2. pip (Python package installer)
3. Git

---

## Installation Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/Canerakcasu/AIRPORTTRACKER.git
cd AIRPORTTRACKER
```

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

## Project Structure
```
AIRPORTTRACKER/
├── flights/
│   ├── views.py  # Contains the logic for handling requests
│   ├── urls.py   # URL routing
│   ├── templates/
│   │   ├── index.html
│   │   ├── search_results.html
├── static/       # Contains static files like CSS and images
├── manage.py     # Django management script
```

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

