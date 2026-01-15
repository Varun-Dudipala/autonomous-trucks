"""
Autonomous Trucks Fleet Management System
Main Flask application with routes and business logic
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import os
import requests
import subprocess
import sys

# Import configuration
from config import Config, get_config

# Import database collections
import db

# Import model functions
from models import (
    get_all_trucks, insert_truck, update_truck_status, delete_truck,
    create_user, validate_user, get_user_data, update_user_profile,
    create_alert, get_alerts, mark_alert_read, mark_alert_acknowledged,
    get_unread_alert_count, add_truck_schedule, create_service_request,
    get_truck_schedules, get_service_requests
)

# Initialize Flask app
app = Flask(__name__)

# Load configuration from environment
config_obj = get_config()
app.config.from_object(config_obj)

# Validate configuration and show warnings
warnings = Config.validate()
if warnings:
    for warning in warnings:
        print(f"⚠️  {warning}")

# Context processor to make Google Maps API key available in all templates
@app.context_processor
def inject_google_maps_api_key():
    return {'google_maps_api_key': Config.GOOGLE_MAPS_API_KEY} 

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if validate_user(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Creating user
        if create_user(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    trucks = get_all_trucks()
    return render_template('index.html', trucks=trucks)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_truck():
    if request.method == 'POST':
        truck_id = request.form['truck_id']
        location_input = request.form['location']
        speed = request.form['speed']
        status = request.form['status']
        
        final_location_coords = None

        # Try to parse as "lat,lng" first
        try:
            parts = location_input.split(',')
            if len(parts) == 2:
                lat = float(parts[0].strip())
                lng = float(parts[1].strip())
                final_location_coords = f"{lat},{lng}"
        except ValueError:
            pass # Not a coordinate string, proceed to geocode

        if final_location_coords is None: # Geocode if not already coordinates
            api_key = app.config.get('GOOGLE_MAPS_API_KEY')
            if not api_key:
                flash('Error: Google API key not configured for geocoding.', 'error')
                return render_template('add_truck.html')

            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location_input.replace(' ', '+')}&key={api_key}"
            
            try:
                response = requests.get(geocode_url)
                response.raise_for_status() # Raise an exception for bad status codes
                geocode_data = response.json()

                if geocode_data.get('status') == 'OK' and geocode_data.get('results'):
                    geom = geocode_data['results'][0]['geometry']['location']
                    final_location_coords = f"{geom['lat']},{geom['lng']}"
                else:
                    flash(f"Could not geocode location: '{location_input}'. Status: {geocode_data.get('status')}", 'error')
                    # Keep original input if geocoding fails, or handle as you see fit
                    final_location_coords = location_input 
            except requests.exceptions.RequestException as e:
                flash(f"Error connecting to geocoding service: {e}", 'error')
                final_location_coords = location_input # Fallback to original input
            except Exception as e:
                flash(f"An unexpected error occurred during geocoding: {e}", "error")
                final_location_coords = location_input


        if final_location_coords: # Ensure we have some location
            insert_truck(truck_id, final_location_coords, speed, status)
            flash('Truck added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            # This case should ideally not be reached if geocoding fallback works
            flash('Failed to determine location for the truck.', 'error')
            
    return render_template('add_truck.html')

@app.route('/update/<truck_id>', methods=['GET', 'POST'])
@login_required
def update_truck(truck_id):
    if request.method == 'POST':
        new_status = request.form['status']
        update_truck_status(truck_id, new_status)
        return redirect(url_for('index'))
    return render_template('update.html', truck_id=truck_id)

@app.route('/delete/<truck_id>')
@login_required
def delete_truck_route(truck_id):
    delete_truck(truck_id)
    return redirect(url_for('index'))

@app.route('/reports')
@login_required
def reports():
    trucks = get_all_trucks()
    return render_template('reports.html', trucks=trucks)

@app.route('/track')
@login_required
def track_trucks():
    trucks = get_all_trucks()
    return render_template('track_trucks.html', trucks=trucks)

@app.route('/track_map')
@login_required
def track_map():
    trucks = get_all_trucks()
    return render_template('track_map.html', trucks=trucks, google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

@app.route('/schedule')
@login_required
def schedule():
    trucks = get_all_trucks()
    all_schedules_raw = get_truck_schedules() 
    
    # Get a set of truck_ids that currently exist
    existing_truck_ids = {truck['truck_id'] for truck in trucks}
    
    # Filter schedules to only include those for existing trucks
    filtered_schedules = [
        sch for sch in all_schedules_raw if sch.get('truck_id') in existing_truck_ids
    ]
    
    return render_template('schedule.html', trucks=trucks, schedules=filtered_schedules)

@app.route('/add_schedule', methods=['POST'])
@login_required
def add_schedule():
    truck_id = request.form['truck_id']
    destination = request.form['destination']
    departure_time = request.form['departure_time']
    arrival_time = request.form['arrival_time']
    
    # Call a function to save the schedule to the database
    add_truck_schedule(truck_id, destination, departure_time, arrival_time)
    flash('Schedule added successfully!', 'success')
    return redirect(url_for('schedule'))

@app.route('/request_service')
@login_required
def request_service():
    trucks = get_all_trucks()
    # Get all service requests from the database
    service_requests = get_service_requests()
    return render_template('request_service.html', trucks=trucks, service_requests=service_requests)

@app.route('/submit_service_request', methods=['POST'])
@login_required
def submit_service_request():
    truck_id = request.form['truck_id']
    service_type = request.form['service_type']
    description = request.form['description']
    requested_date = request.form['requested_date']
    
    # Call a function to save the service request to the database
    create_service_request(truck_id, service_type, description, requested_date, session['username'])
    flash('Service request submitted successfully!', 'success')
    return redirect(url_for('request_service'))

@app.route('/profile')
@login_required
def profile():
    user_data = get_user_data(session['username'])
    return render_template('profile.html', user=user_data)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    full_name = request.form.get('full_name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    
    # Call a function to update the user profile in the database
    update_user_profile(session['username'], full_name, email, phone)
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/simulation')
@login_required
def simulation():
    trucks = get_all_trucks()
    return render_template('simulation.html', trucks=trucks)

@app.route('/run_simulation', methods=['POST'])
@login_required
def run_simulation():
    truck_id = request.form['truck_id']
    simulation_type = request.form['simulation_type']
    # duration = request.form['duration'] # Kept in HTML, not used in this backend logic yet

    trucks_for_dropdown = get_all_trucks() # For re-rendering the form
    simulation_results = None
    error_message = None

    if simulation_type == "carla_automatic":
        # Paths for CARLA
        carla_root = r"C:\Users\varun\Downloads\CARLA_0.9.14\WindowsNoEditor"
        carla_api_path = os.path.join(carla_root, "PythonAPI")
        carla_egg_name = "carla-0.9.14-py3.7-win-amd64.egg"
        carla_egg_path = os.path.join(carla_api_path, "carla", "dist", carla_egg_name)
        carla_examples_path = os.path.join(carla_api_path, "examples")
        
        automatic_control_script = os.path.join(carla_examples_path, "automatic_control.py")
        generate_traffic_script = os.path.join(carla_examples_path, "generate_traffic.py")

        if not os.path.exists(carla_egg_path):
            return jsonify({"status": "error", "message": f"CARLA egg file not found: {carla_egg_path}"})
        if not os.path.exists(automatic_control_script):
            return jsonify({"status": "error", "message": f"CARLA automatic_control.py script not found: {automatic_control_script}"})
        if not os.path.exists(generate_traffic_script):
            return jsonify({"status": "error", "message": f"CARLA generate_traffic.py script not found: {generate_traffic_script}"})

        # Construct PYTHONPATH
        env = os.environ.copy()
        current_python_path = env.get("PYTHONPATH", "")
        # Ensure carla_api_path (which contains 'agents' etc.) is also in PYTHONPATH
        env["PYTHONPATH"] = f"{carla_egg_path}{os.pathsep}{carla_api_path}{os.pathsep}{carla_examples_path}{os.pathsep}{current_python_path}"

        python_executable = sys.executable 

        # Command for automatic_control.py (our hero vehicle)
        hero_command = [
            python_executable,
            automatic_control_script,
            "--filter", "vehicle.tesla.cybertruck",
            "--loop",
            "--sync"  # Explicitly run hero in sync mode
            # Add other arguments like --host, --port, --agent, --behavior, --seed if needed
        ]

        # Command for generate_traffic.py (NPCs)
        traffic_command = [
            python_executable,
            generate_traffic_script,
            "-n", "30",  # Number of vehicles
            "-w", "10",  # Number of walkers
            # "--asynch", # Let's try synchronous mode first for better coordination.
            # The generate_traffic.py script has logic to become sync master if needed.
            # Add --tm-port if necessary, defaults to 8000
            # Add --seed for deterministic traffic if desired
        ]

        try:
            # Start the traffic script first
            # It might try to set synchronous mode for the server
            process_traffic = subprocess.Popen(traffic_command, env=env)
            # Potentially add a small delay if needed for traffic manager to initialize
            # import time
            # time.sleep(5) # Example: wait 5 seconds

            # Start the hero vehicle script
            process_hero = subprocess.Popen(hero_command, env=env)
            
            # Store process handles if you need to manage them later (e.g., terminate)
            # For now, we're just launching them.
            # session['carla_processes'] = {'traffic': process_traffic.pid, 'hero': process_hero.pid}

            flash('CARLA simulation with traffic started! Ensure CARLA server is running.', 'success')
            return redirect(url_for('simulation'))
        except FileNotFoundError:
            error_message = "Error: CARLA script or python executable not found."
        except Exception as e:
            error_message = f"Error launching CARLA simulation: {e}"
        
        if error_message:
            flash(error_message, 'error')
        return render_template('simulation.html', trucks=trucks_for_dropdown, results=None)


    # Existing Google Maps based simulation logic
    selected_truck = trucks_collection.find_one({"truck_id": truck_id})
    if not selected_truck:
        error_message = f"Truck with ID '{truck_id}' not found."
    elif 'location' not in selected_truck or ',' not in selected_truck['location']:
        error_message = f"Truck '{truck_id}' does not have valid coordinates for its current location."
    else:
        current_location_str = selected_truck['location']
        schedules = get_truck_schedules(truck_id=truck_id)
        if not schedules:
            error_message = f"No schedule found for truck '{truck_id}' to determine destination."
        else:
            destination_str = schedules[0].get('destination')
            if not destination_str:
                error_message = f"Schedule for truck '{truck_id}' is missing a destination."
            else:
                api_key = app.config.get('GOOGLE_MAPS_API_KEY')
                if not api_key:
                    error_message = "Google API key not configured."
                else:
                    avoid_options = []
                    if simulation_type == 'route':
                        # If 'highway' is not checked (not present or not 'true'), avoid highways.
                        if request.form.get('highway') != 'true': 
                            avoid_options.append('highways')
                        # If 'tolls' is not checked (not present or not 'true'), avoid tolls.
                        if request.form.get('tolls') != 'true':
                            avoid_options.append('tolls')

                    avoid_param = '|'.join(avoid_options)
                    
                    directions_url_base = (
                        f"https://maps.googleapis.com/maps/api/directions/json?"
                        f"origin={current_location_str}&destination={destination_str.replace(' ', '+')}&key={api_key}"
                    )
                    if avoid_param:
                        directions_url = f"{directions_url_base}&avoid={avoid_param}"
                    else:
                        directions_url = directions_url_base

                    try:
                        response = requests.get(directions_url)
                        response.raise_for_status()
                        directions_data = response.json()

                        if directions_data.get('status') == 'OK' and directions_data.get('routes'):
                            route = directions_data['routes'][0]['legs'][0]
                            distance_meters = route['distance']['value']
                            duration_seconds = route['duration']['value']
                            distance_km = distance_meters / 1000.0
                            duration_min = duration_seconds / 60.0

                            if simulation_type == 'fuel':
                                fuel_liters = distance_km / AVERAGE_FUEL_EFFICIENCY_KM_PER_L
                                simulation_results = {
                                    'distance_km': round(distance_km, 2),
                                    'duration_min': round(duration_min, 1),
                                    'fuel_liters': round(fuel_liters, 2),
                                    'truck_id': truck_id,
                                    'destination': destination_str,
                                    'type': 'Fuel Efficiency'
                                }
                            elif simulation_type == 'route':
                                simulation_results = {
                                    'distance_km': round(distance_km, 2),
                                    'duration_min': round(duration_min, 1),
                                    'truck_id': truck_id,
                                    'destination': destination_str,
                                    'type': 'Route Optimization',
                                    'avoided': avoid_param if avoid_param else "None"
                                }
                        else:
                            error_message = f"Could not get directions. Status: {directions_data.get('status')}. Origin: {current_location_str}, Dest: {destination_str}, Avoid: {avoid_param}"
                    except requests.exceptions.RequestException as e:
                        error_message = f"Error connecting to Directions API: {e}"
                    except Exception as e:
                        error_message = f"An unexpected error occurred: {e}"
    
    # This specific error message for unimplemented types is less critical now since UI is restricted,
    # but kept as a safeguard for direct/unexpected POST requests.
    if not simulation_results and not error_message:
        if simulation_type not in ['fuel', 'route', 'carla_automatic']:
             error_message = f"Simulation type '{simulation_type}' is not supported."

    if error_message:
        flash(error_message, 'error')

    return render_template('simulation.html', trucks=trucks_for_dropdown, results=simulation_results)

# Add this context processor to make unread alert count available in all templates
@app.context_processor
def inject_alert_count():
    if 'username' in session:
        return {'unread_alert_count': get_unread_alert_count()}
    return {'unread_alert_count': 0}

@app.route('/alerts')
@login_required
def alerts_dashboard():
    severity_filter = request.args.get('severity')
    truck_id_filter = request.args.get('truck_id')
    
    # Get all trucks for the filter dropdown
    trucks = get_all_trucks()
    
    # Get filtered alerts
    alerts = get_alerts(
        truck_id=truck_id_filter,
        severity=severity_filter
    )
    
    return render_template(
        'alerts.html',
        alerts=alerts,
        trucks=trucks,
        active_severity=severity_filter,
        active_truck=truck_id_filter
    )

@app.route('/alerts/mark_read/<alert_id>')
@login_required
def mark_read(alert_id):
    mark_alert_read(alert_id)
    return redirect(url_for('alerts_dashboard'))

@app.route('/alerts/acknowledge/<alert_id>')
@login_required
def acknowledge_alert(alert_id):
    mark_alert_acknowledged(alert_id)
    flash('Alert acknowledged', 'success')
    return redirect(url_for('alerts_dashboard'))

@app.route('/alerts/test', methods=['POST'])
@login_required
def create_test_alert():
    # For testing - creates a sample alert
    truck_id = request.form.get('truck_id')
    severity = request.form.get('severity', 'medium')
    
    create_alert(
        alert_type="test",
        truck_id=truck_id,
        message=f"Test alert for truck {truck_id}",
        severity=severity
    )
    
    flash('Test alert created', 'success')
    return redirect(url_for('alerts_dashboard'))

@app.route('/api/truck_schedule/<truck_id>')
@login_required
def get_truck_schedule_api(truck_id):
    schedules = get_truck_schedules(truck_id=truck_id) 
    if schedules:
        schedule_data = schedules[0]
        # Convert ObjectId to string for JSON serialization
        if '_id' in schedule_data and hasattr(schedule_data['_id'], '__str__'):
            schedule_data['_id'] = str(schedule_data['_id'])
        return jsonify(schedule_data)
    return jsonify({"error": "No schedule found for this truck"}), 404

if __name__ == '__main__':
    # Run the application with configuration from environment
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )