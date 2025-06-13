from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

# Load the environ variables
load_dotenv()
class DatabaseConnection:
    __conn_string: str | None = os.getenv("MONGO_URI")

    def __init__(self) -> None:
        self.connected = False

        try:
            # connect the database
            self.client = MongoClient(self.__conn_string)
            
            # get the database
            self.db = self.client["coRider"]

            # get the collection
            self.users_collection = self.db["users"]

            self.connected = True
            print("Database is connected")

        except Exception as e:
            print(f"Mongodb connection error: {e}")
            self.connected = False


    def is_connected(self):
        return self.connected

    def initialize_collection(self):
        if not self.connected:
            raise Exception("Database not connected")
        self.users_collection.create_index("email", unique=True)


    def find_users(self):
        if not self.connected:
            raise Exception("Database not connected")
        return self.users_collection.find({})
    
    def clear_collection(self):
        if not self.connected:
            raise Exception("Database not connected")
        self.users_collection.delete_many({})


    def store_payload(self, payload: dict) -> str:
        if not self.connected:
            raise Exception("Database not connected")
        try:
            result = self.users_collection.insert_one(payload)
            print(result)
            return str(result.inserted_id)
        except Exception as e:
            return f"Error while inserting data: {e}"
    

    def close_connection(self):
        if self.client:
            self.client.close()


db = DatabaseConnection()
# db.store_payload(user_data1)
# db.store_payload(user_data)
# db.clear_collection()
# db.close_connection()

@app.route("/")
def test():
    if not db.is_connected():
        return jsonify({
            "Message": "Database is not connected",
        }), 500
    return "<p>testing environment</p>"


@app.get("/users")
def fetch_users():
    """
    fetch all the users from the database
    """
    if not db.is_connected():
        return jsonify({
            "Message": "Database is not connected",
        }), 500

    users = db.find_users()
    results = []
    for user in users:
        user["_id"] = str(user["_id"])
        results.append(user)
    return jsonify(results)


@app.post("/users")
def post_user():
    if not db.is_connected():
        return jsonify({
            "Message": "Database is not connected",
        }), 500

    req_data = request.get_json()
    name = req_data["name"]
    username = req_data["username"]
    password = req_data["password"]
        
    payload = {
        "name": name,
        "username": username,
        "password": password,
    }

    insert_result = db.store_payload(payload)
    return f"Inserted Id: {insert_result}"


@app.get("/users/<id>")
def get_user(id: str):
    """
    fetch a specific user from the database provide user_id
    """

    try:
        if not db.is_connected():
            return jsonify({
                "Message": "Database is not connected",
            }), 500

        user = db.users_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({f"Error: Error while getting ther user {str(e)}"})



@app.delete("/users/<id>")
def delete_user(id: str):
    try:
        if not db.is_connected():
            return jsonify({
                "Message": "Database is not connected",
            }), 500

        db.users_collection.delete_one({"_id": ObjectId(id)})
        return jsonify({"Message": "Deleted user successfully"})
    except Exception as e:
        return jsonify({
            "Message": str(e)
        }), 500

@app.put("/users/<id>")
def update_user(id: str):
    try:
        if not db.is_connected():
            return jsonify({
                "Message": "Database is not connected",
            }), 500

        req = request.get_json()
        query_filter = {
            "_id": ObjectId(id), 
        }

        update_operation = {
            "$set": {
                "name": req["name"],
                "username": req["username"],
                "password": req["password"],
            }
        }
        db.users_collection.update_one(query_filter, update_operation)
        return jsonify({"Message":"Update successful"})
    except Exception as e:
        return jsonify({
            "Message": str(e),
        }), 500
# db.close_connection()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
