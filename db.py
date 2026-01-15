"""
Database module for MongoDB connection and collections
Uses configuration from config.py
"""

import pymongo
from config import Config

# MongoDB connection using environment variables
client = pymongo.MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DATABASE]

# Collections
trucks_collection = db["trucks"]
users_collection = db["users"]
schedules_collection = db["schedules"]
service_requests_collection = db["service_requests"]
alerts_collection = db["alerts"]