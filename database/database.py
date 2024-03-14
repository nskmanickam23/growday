def mongo_conn():
    import motor.motor_asyncio
    uri = "mongodb+srv://giri1208srinivas:mongouser@cluster0.extptud.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You have successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client


# User.create_index([("email", pymongo.ASCENDING)], unique=True)
from pymongo import MongoClient


class Database:
    def __init__(self, mongo_uri, db_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def check_connection(self):
        try:
            self.client.server_info()  # Check if the server is available
            return True
        except Exception as e:
            return False

    def collection_exists(self, collection_name):
        return collection_name in self.db.list_collection_names()


# Configuration settings
MONGO_URI = "mongodb+srv://giri1208srinivas:mongouser@cluster0.extptud.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "growday"

# Create a global instance of the database connection
database = Database(MONGO_URI, DB_NAME)
print(database)
