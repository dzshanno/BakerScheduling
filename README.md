# BakerScheduling

planned direcory structure

bakery_scheduler/
│
├── app/
│   ├── __init__.py             # Create and configure the app
│   ├── models.py               # Database models
│   ├── routes.py               # Application routes (main endpoints)
│   ├── forms.py                # Optional, for forms (e.g., login)
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base template (layout)
│   │   ├── index.html          # Homepage template
│   │   └── ...                 # Other templates
│   ├── static/                 # Static assets (CSS, JS, images)
│   │   ├── css/
│   │   │   └── styles.css      # CSS stylesheets
│   │   ├── js/
│   │   │   └── app.js          # JavaScript files
│   │   └── images/             # Image files
│   ├── blueprints/             # Folder for blueprints (e.g., auth)
│   │   └── auth/               # Example auth blueprint
│   │       ├── __init__.py     # Initializes the auth blueprint
│   │       ├── routes.py       # Auth routes (e.g., login, logout)
│   │       └── templates/      # Templates specific to auth (e.g., login.html)
│   └── config.py               # Configuration settings
│
├── migrations/                 # Migration scripts (generated by Flask-Migrate)
│
├── .env                        # Environment variables
├── .flaskenv                   # Flask environment variables (e.g., FLASK_APP)
├── .gitignore                  # Git ignore file
├── requirements.txt            # Dependencies for the project
├── Procfile                    # Deployment settings (e.g., for Heroku)
└── run.py                      # Entry point to run the Flask application
