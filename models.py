"""
Database models and business logic for the fleet management system
Contains functions for CRUD operations on trucks, users, schedules, service requests, and alerts
"""

from werkzeug.security import generate_password_hash, check_password_hash
import db

def get_all_trucks():
    """Get all trucks from the database"""
    return list(db.db.trucks_collection.find({}, {"_id": 0}))

def insert_truck(truck_id, location, speed, status):
    truck_data = {
        "truck_id": truck_id,
        "location": location,
        "speed": speed,
        "status": status
    }
    db.trucks_collection.insert_one(truck_data)

def update_truck_status(truck_id, new_status):
    db.trucks_collection.update_one(
        {"truck_id": truck_id},
        {"$set": {"status": new_status}}
    )

def delete_truck(truck_id):
    # Delete the truck itself from the db.trucks_collection
    db.trucks_collection.delete_one({"truck_id": truck_id})
    # Also delete any schedules associated with this truck_id from the schedules_collection
    db.schedules_collection.delete_many({"truck_id": truck_id})

def create_user(username, password):
    # Checking if user already exists
    existing_user = db.users_collection.find_one({'username': username})
    if existing_user:
        return False
    
    # Hash password
    hashed_password = generate_password_hash(password)
    
    # Inserting new user
    db.users_collection.insert_one({
        'username': username,
        'password': hashed_password
    })
    return True

def validate_user(username, password):
    # Finding user
    user = db.users_collection.find_one({'username': username})
    
    # Checking if user exists and password is correct
    if user and check_password_hash(user['password'], password):
        return True
    return False

def add_truck_schedule(truck_id, destination, departure_time, arrival_time):
    schedule_data = {
        "truck_id": truck_id,
        "destination": destination,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "status": "Scheduled"
    }
    db.schedules_collection.insert_one(schedule_data)

def get_truck_schedules(truck_id=None):
    if truck_id:
        return list(db.schedules_collection.find({"truck_id": truck_id}))
    return list(db.schedules_collection.find({}))

def create_service_request(truck_id, service_type, description, requested_date, username):
    service_data = {
        "truck_id": truck_id,
        "service_type": service_type,
        "description": description,
        "requested_date": requested_date,
        "requested_by": username,
        "status": "Pending"
    }
    db.service_requests_collection.insert_one(service_data)

def get_service_requests(truck_id=None):
    if truck_id:
        return list(db.service_requests_collection.find({"truck_id": truck_id}, {"_id": 0}))
    return list(db.service_requests_collection.find({}, {"_id": 0}))

def get_user_data(username):
    user = db.users_collection.find_one({'username': username}, {'_id': 0, 'password': 0})
    return user

def update_user_profile(username, full_name, email, phone):
    db.users_collection.update_one(
        {"username": username},
        {"$set": {
            "full_name": full_name,
            "email": email,
            "phone": phone
        }}
    )

def create_alert(alert_type, truck_id, message, severity, timestamp=None):
    """
    Create a new alert in the database
    
    Parameters:
    - alert_type: Type of alert (maintenance, safety, operational, etc.)
    - truck_id: ID of the truck the alert is for
    - message: Alert message content
    - severity: Alert severity (high, medium, low)
    - timestamp: Time the alert was generated, defaults to current time
    """
    from datetime import datetime
    
    if timestamp is None:
        timestamp = datetime.now()
        
    alert_data = {
        "alert_type": alert_type,
        "truck_id": truck_id,
        "message": message,
        "severity": severity,
        "timestamp": timestamp,
        "read": False,
        "acknowledged": False
    }
    
    return db.alerts_collection.insert_one(alert_data)

def get_alerts(truck_id=None, unread_only=False, severity=None, limit=50):
    """
    Get alerts from the database with optional filtering
    
    Parameters:
    - truck_id: Optional filter for specific truck
    - unread_only: If True, only return unread alerts
    - severity: Optional filter by severity level
    - limit: Maximum number of alerts to return
    """
    query = {}
    
    if truck_id:
        query["truck_id"] = truck_id
        
    if unread_only:
        query["read"] = False
        
    if severity:
        query["severity"] = severity
    
    return list(db.alerts_collection.find(
        query
    ).sort("timestamp", -1).limit(limit))

def mark_alert_read(alert_id):
    """Mark an alert as read"""
    from bson.objectid import ObjectId
    db.alerts_collection.update_one(
        {"_id": ObjectId(alert_id)},
        {"$set": {"read": True}}
    )

def mark_alert_acknowledged(alert_id):
    """Mark an alert as acknowledged"""
    from bson.objectid import ObjectId
    db.alerts_collection.update_one(
        {"_id": ObjectId(alert_id)},
        {"$set": {"acknowledged": True}}
    )

def get_unread_alert_count():
    """Return the number of unread alerts"""
    return db.alerts_collection.count_documents({"read": False})