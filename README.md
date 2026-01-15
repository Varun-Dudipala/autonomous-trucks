# Autonomous Trucks Fleet Management System

![Status](https://img.shields.io/badge/Status-Active_Development-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-4.0+-green?logo=mongodb)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive web-based fleet management system for monitoring, tracking, and managing autonomous trucks. Real-time tracking with Google Maps, intelligent scheduling, maintenance alerts, and full user management.

> **Add these topics to your GitHub repo**: `fleet-management`, `autonomous-vehicles`, `logistics`, `python`, `flask`, `mongodb`, `real-time-tracking`, `google-maps`, `web-application`, `transportation`, `iot`, `dashboard`

## Features

### Core Fleet Management
- **Real-time Truck Tracking** - Monitor truck locations on interactive Google Maps
- **Fleet Dashboard** - Overview of fleet status, active trucks, and alerts at a glance
- **Truck Management** - Add, update, and delete trucks from the fleet
- **Status Monitoring** - Track truck status (Active, Maintenance, Idle, En Route)

### Operations
- **Route Scheduling** - Schedule routes and deliveries with departure/arrival times
- **Service Requests** - Request and track maintenance and service for trucks
- **Alert System** - Real-time alerts with severity levels (high, medium, low)
- **Reports & Analytics** - Generate reports on fleet performance and truck status

### User Management
- **Secure Authentication** - Session-based login with password hashing (Werkzeug)
- **User Profiles** - Manage user information and preferences
- **Role-based Access** - Login-required decorator for protected routes

### Advanced Features
- **Simulation Integration** - Carla 0.9.14 integration for testing scenarios
- **Multi-Collection Database** - Organized data structure with MongoDB
- **Responsive UI** - Modern dashboard with CSS styling
- **Real-time Updates** - Live fleet status and alert notifications

## Screenshots

*Coming soon - Dashboard and tracking interface screenshots will be added here*

| Dashboard | Map Tracking | Alerts |
|-----------|--------------|--------|
| ![Dashboard](screenshots/dashboard.png) | ![Map](screenshots/map.png) | ![Alerts](screenshots/alerts.png) |

## Tech Stack

### Backend
- **Flask 3.0** - Lightweight Python web framework
- **PyMongo** - MongoDB driver for Python
- **Werkzeug** - Password hashing and security utilities

### Database
- **MongoDB 4.0+** - NoSQL database with 5 collections:
  - `trucks` - Fleet vehicle data
  - `users` - User accounts and profiles
  - `schedules` - Route scheduling
  - `service_requests` - Maintenance tracking
  - `alerts` - Real-time alert system

### Frontend
- **Jinja2 Templates** - Server-side rendering with template inheritance
- **HTML5/CSS3** - Responsive, modern UI
- **JavaScript** - Interactive features
- **Google Maps API** - Real-time location tracking

### Simulation
- **Carla 0.9.14** - Autonomous vehicle simulation platform

## Architecture

```
autonomous_trucks/
├── app.py                    # Flask application & routes (515 lines)
├── models.py                 # Database models & business logic
├── db.py                     # MongoDB connection & collections
├── config.py                 # Configuration management
├── static/
│   └── styles.css           # UI styling (12KB)
├── templates/               # 14 Jinja2 templates
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Dashboard with fleet summary
│   ├── track_map.html       # Google Maps tracking interface
│   ├── track_trucks.html    # List view of truck locations
│   ├── schedule.html        # Route scheduling
│   ├── request_service.html # Maintenance requests
│   ├── alerts.html          # Alert management
│   ├── reports.html         # Analytics & reports
│   ├── simulation.html      # Simulation controls
│   ├── add_truck.html       # Add new truck form
│   ├── update.html          # Update truck status
│   ├── login.html           # User login
│   ├── register.html        # User registration
│   └── profile.html         # User profile management
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## Installation

### Prerequisites

- **Python 3.7+** - Programming language
- **MongoDB 4.0+** - Database server
- **Google Maps API Key** - For location tracking
- **Carla 0.9.14** (Optional) - For simulation features

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/varun-dudipala/autonomous-trucks.git
   cd autonomous-trucks
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**
   ```bash
   # Install MongoDB (if not already installed)
   # macOS: brew install mongodb-community
   # Ubuntu: sudo apt install mongodb

   # Start MongoDB service
   # macOS: brew services start mongodb-community
   # Ubuntu: sudo systemctl start mongodb

   # Verify MongoDB is running on localhost:27017
   mongo --eval "db.version()"
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your credentials:
   # - GOOGLE_MAPS_API_KEY
   # - SECRET_KEY
   # - MONGODB_URI (optional, defaults to localhost)
   ```

6. **Get Google Maps API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Maps JavaScript API
   - Create API key
   - Add key to `.env` file

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open browser to `http://localhost:5000`
   - Register a new account
   - Start managing your fleet!

## Usage

### Getting Started

1. **Register/Login**: Create an account at `/register` or login at `/login`
2. **Add Trucks**: Navigate to "Add Truck" and enter truck details
3. **View Dashboard**: Main dashboard shows fleet overview with statistics
4. **Track Trucks**: Use map view or list view to monitor locations

### Route Management

- **Schedule Route**: Go to Schedule page, select truck, enter destination and times
- **View Schedules**: See all scheduled routes with departure/arrival times
- **Update Status**: Mark routes as completed or in-progress

### Maintenance

- **Request Service**: Submit service requests with type (maintenance, repair, inspection)
- **Track Requests**: View all service requests and their status (Pending, In Progress, Completed)
- **View Alerts**: Monitor maintenance alerts and critical notifications

### Analytics

- **Reports**: Generate fleet performance reports
- **Alert History**: View past alerts and their severity
- **Simulation**: Run test scenarios to validate fleet behavior

## API Routes

### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Fleet Management
- `GET /` - Dashboard (requires login)
- `GET/POST /add` - Add new truck
- `POST /update/<truck_id>` - Update truck status
- `POST /delete/<truck_id>` - Delete truck

### Tracking
- `GET /track_trucks` - List view of trucks
- `GET /track_map` - Map view with Google Maps

### Operations
- `GET/POST /schedule` - Manage schedules
- `GET/POST /request_service` - Service requests
- `GET /alerts` - View and manage alerts

### User
- `GET/POST /profile` - User profile management

### Analytics
- `GET /reports` - Fleet reports
- `GET /simulation` - Simulation interface

## Configuration

Edit `config.py` or use environment variables:

```python
# Database
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "autonomous_trucks"

# Google Maps
GOOGLE_MAPS_API_KEY = "your_api_key_here"

# Flask
SECRET_KEY = "your_secret_key_here"
DEBUG = False
HOST = "0.0.0.0"
PORT = 5000

# Simulation
CARLA_HOST = "localhost"
CARLA_PORT = 2000
```

## Database Schema

### Trucks Collection
```javascript
{
  "truck_id": "string",
  "location": "string",
  "speed": "number",
  "status": "Active|Maintenance|Idle|En Route"
}
```

### Users Collection
```javascript
{
  "username": "string",
  "password": "hashed_string",
  "full_name": "string",
  "email": "string",
  "phone": "string"
}
```

### Schedules Collection
```javascript
{
  "truck_id": "string",
  "destination": "string",
  "departure_time": "datetime",
  "arrival_time": "datetime",
  "status": "Scheduled|In Progress|Completed"
}
```

### Service Requests Collection
```javascript
{
  "truck_id": "string",
  "service_type": "Maintenance|Repair|Inspection",
  "description": "string",
  "requested_date": "datetime",
  "requested_by": "string",
  "status": "Pending|In Progress|Completed"
}
```

### Alerts Collection
```javascript
{
  "alert_type": "maintenance|safety|operational",
  "truck_id": "string",
  "message": "string",
  "severity": "high|medium|low",
  "timestamp": "datetime",
  "read": "boolean",
  "acknowledged": "boolean"
}
```

## Security Features

- **Password Hashing**: Werkzeug's `generate_password_hash` and `check_password_hash`
- **Session Management**: Flask sessions with secure secret key
- **Protected Routes**: `@login_required` decorator for authenticated access
- **Environment Variables**: Sensitive data stored in `.env` file
- **Input Validation**: Form validation on registration and data entry

## Performance Considerations

- **MongoDB Indexing**: Consider adding indexes on frequently queried fields
- **Connection Pooling**: MongoDB client handles connection pooling automatically
- **Caching**: Can add Redis for session caching in production
- **Load Balancing**: Use Gunicorn + Nginx for production deployment

## What I Learned

- **Full-stack development** with Flask and MongoDB
- **Real-time tracking** systems with Google Maps API
- **Database design** for complex relationships (trucks, schedules, alerts)
- **User authentication** and session management
- **RESTful API design** principles
- **Template inheritance** with Jinja2
- **IoT integration patterns** for vehicle tracking
- **Alert systems** with severity levels and notifications

## Future Enhancements

- [ ] WebSocket integration for real-time updates
- [ ] Mobile app for drivers (React Native)
- [ ] AI-powered route optimization
- [ ] Predictive maintenance using ML
- [ ] Integration with telematics devices
- [ ] Multi-tenant support for fleet operators
- [ ] Advanced analytics dashboard with charts
- [ ] Email/SMS notifications for critical alerts
- [ ] Export reports to PDF/CSV
- [ ] API for third-party integrations

## Deployment

### Production Deployment

**Using Gunicorn + Nginx:**

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Docker Deployment:**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Cloud Platforms:**
- **Heroku**: Use Procfile with Gunicorn
- **AWS EC2**: Deploy with Nginx reverse proxy
- **Google Cloud Run**: Containerized deployment
- **Railway**: Simple git-based deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Maps API for location tracking
- Carla Simulator for autonomous vehicle testing
- Flask framework and MongoDB for robust backend

---

**Built with Flask, MongoDB, and Google Maps API**
