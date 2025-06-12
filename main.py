from enum import unique
from flask import Flask
import os
from dotenv import load_dotenv
from pymongo import MongoClient

app = Flask(__name__)

# Load the environ variables
load_dotenv()

user_data: dict = {
    "_id": 1,
    "name": "Alex",
    "username": "Alex@gmail.com",
    "password": "Alex!@#1234",
}

user_data1: dict = {
    "_id": 2,
    "name": "Alex Homorazu",
    "username": "Alexhom@gmail.com",
    "password": "Alex!@#1234",
}


class DatabaseConnection:
    __conn_string: str | None = os.getenv("MONGO_URI")

    def __init__(self):
        try:
            # connect the database
            self.client = MongoClient(self.__conn_string)
            
            # get the database
            self.db = self.client["coRider"]

            # get the collection
            self.users_collection = self.db["users"]
        except Exception as e:
            return f"Mongodb connection error: {e}"
   

    def initialize_collection(self):
        self.users_collection.create_index(["_id", "email"], unique=True)

    
    def clear_collection(self):
        self.users_collection.delete_many({})


    def store_payload(self, payload):
        try:
            result = self.users_collection.insert_one(payload)
            print(result)
        except Exception as e:
            return f"Error while inserting data: {e}"
    

    def close_connection(self):
        self.client.close()


db = DatabaseConnection()
# db.store_payload(user_data1)
# db.clear_collection()
# db.close_connection()

@app.route("/")
def test():
    return "<p>testing environment</p>"


@app.get("/users/id")
def get_user(id):
    """
    fetch a specific user from the database provide user_id
    """
    try:
        return db.users_collection.find_one({"_id": id})
    except:
        return None


@app.get("/users")
def fetch_users():
    """
    fetch all the users from the database
    """
    return list(db.users_collection.find({}))


if __name__ == "__main__":
    app.run(debug=True)
