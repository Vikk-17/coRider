from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

# Load the environ variables
load_dotenv()

# user_data: dict = {
#     "name": "Alex",
#     "username": "Alex@gmail.com",
#     "password": "Alex!@#1234",
# }
#
# user_data1: dict = {
#     "name": "Alex Homorazu",
#     "username": "Alexhom@gmail.com",
#     "password": "Alex!@#1234",
# }


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
        self.users_collection.create_index("email", unique=True)

    
    def clear_collection(self):
        self.users_collection.delete_many({})


    def store_payload(self, payload: dict) -> str:
        try:
            result = self.users_collection.insert_one(payload)
            print(result)
            return str(result.inserted_id)
        except Exception as e:
            return f"Error while inserting data: {e}"
    

    def close_connection(self):
        self.client.close()


db = DatabaseConnection()
# db.store_payload(user_data1)
# db.store_payload(user_data)
# db.clear_collection()
# db.close_connection()

@app.route("/")
def test():
    return "<p>testing environment</p>"



@app.get("/users")
def fetch_users():
    """
    fetch all the users from the database
    """
    # if request.method == "GET":
    users = db.users_collection.find({})
    results = []
    for user in users:
        user["_id"] = str(user["_id"])
        results.append(user)
    return jsonify(results)


@app.post("/users")
def post_user():
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
    db.users_collection.delete_one({"_id": ObjectId(id)})
    return "Deleted user successfully"

@app.put("/users/<id>")
def update_user(id: str):
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
    return f"Update successful"

# db.close_connection()

if __name__ == "__main__":
    app.run(debug=True)
