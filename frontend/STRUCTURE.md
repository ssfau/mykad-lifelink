mykad-lifelink/
├── backend/
│   ├── core/               # App configuration & security
│   ├── routers/            # API endpoints (e.g., /scan, /patient)
│   └── main.py             # The "Start" file for Python
└── frontend/
    ├── index.html          # Role Selection (Keep this in the root)
    ├── pages/              # Specific screens
    │   ├── doctor.html     # Emergency Dashboard
    │   ├── patient.html    # Registration & Data
    │   └── admin.html      # Clinic Staff portal
    ├── css/                
    │   └── style.css       # Your design file
    ├── js/                 
    │   ├── api.js          # Fetch functions (to talk to Python)
    │   └── ui.js           # Button clicks & screen changes
    └── assets/             # Logos and MyKad icons