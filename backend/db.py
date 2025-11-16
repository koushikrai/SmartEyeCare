from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import os
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "smarteyecare")

# Global MongoDB client and database
client = None
db = None

def get_db():
    """Get MongoDB database connection"""
    global client, db
    if db is None:
        try:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Test connection
            client.admin.command('ping')
            db = client[DATABASE_NAME]
            # Create indexes for better performance
            try:
                db.users.create_index("email", unique=True)
            except Exception:
                # Index might already exist
                pass
            print(f"Connected to MongoDB: {DATABASE_NAME}")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            print(f"MongoDB URI: {MONGODB_URI}")
            print("Please ensure MongoDB is running or check your connection string in .env file")
            raise ConnectionFailure(f"Could not connect to MongoDB: {e}")
    return db

def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

