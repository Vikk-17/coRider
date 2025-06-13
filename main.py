from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

# Load the environ variables
load_dotenv()
class DatabaseConnection:
    """
    A class to connect with mongodb database
    """
    __conn_string: str | None = os.getenv("MONGO_URI")

    def __init__(self) -> None:
        """
        Initialization of db, collection
        returns: None
        """
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


    def is_connected(self) -> bool:
        """
        To check whether the connection is established
        returns: boolean
        """
        return self.connected

    def initialize_collection(self) -> None:
        """
        Initialze the collection in the database with unique email
        return: None
        """
        if not self.connected:
            raise Exception("Database not connected")
        self.users_collection.create_index("email", unique=True)


    def find_users(self):
        """
        Function to fetch all the users
        returns: Cursor to the documents the matces the query
        """
        if not self.connected:
            raise Exception("Database not connected")
        return self.users_collection.find({})
    
    def clear_collection(self) -> None:
        """
        To clean the documents inside the collection
        """
        if not self.connected:
            raise Exception("Database not connected")
        self.users_collection.delete_many({})


    def store_payload(self, payload: dict) -> str:
        """
        To store the payload provided by the user
        params: dictionary 
        returns: str: id of the inserted document
        """
        if not self.connected:
            raise Exception("Database not connected")
        try:
            result = self.users_collection.insert_one(payload)
            print(result)
            return str(result.inserted_id)
        except Exception as e:
            return f"Error while inserting data: {e}"
    

    def close_connection(self):
        """
        To close the connection of the database
        """
        if self.client:
            self.client.close()

# Establish the database connection
db = DatabaseConnection()


"""
# Testing
# db.store_payload(user_data1)
# db.store_payload(user_data)
# db.clear_collection()
# db.close_connection()
"""


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
    return jsonify(results), 200


@app.post("/users")
def post_user():
    """
    Post the data and insert into the database's users collection
    POST /users
    params: json body consist of name, username, password
    returns: id of the inserted payload
    """
    if not db.is_connected():
        return jsonify({
            "Message": "Database is not connected",
        }), 500

    # get the user data 
    req_data = request.get_json()
    
    # generating the payload
    payload = {
        "name": req_data["name"],
        "username": req_data["username"],
        "password": req_data["password"],
    }
    
    # insert the data into the user collection
    insert_result = db.store_payload(payload)
    return jsonify({
        f"Inserted Id: {insert_result}"
    }), 200


@app.get("/users/<id>")
def get_user(id: str):
    """
    fetch a specific user from the database provide user_id
    params: user id 
    returns: jsnonified data of a particular user
    """

    try:
        if not db.is_connected():
            return jsonify({
                "Message": "Database is not connected",
            }), 500
        
        # find the data provied the id
        user = db.users_collection.find_one({"_id": ObjectId(id)})

        if user:
            user["_id"] = str(user["_id"])
            return jsonify(user), 200

        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({
            f"Error: Error while getting ther user {str(e)}"
        }), 500



@app.delete("/users/<id>")
def delete_user(id: str):
    """
    To delete user from the db's user collection
    params: user id 
    returns: jsonified string saying deletion successful
    """
    try:
        if not db.is_connected():
            return jsonify({
                "Message": "Database is not connected",
            }), 500

        db.users_collection.delete_one({"_id": ObjectId(id)})
        return jsonify({
            "Message": "Deleted user successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "Message": str(e)
        }), 500

@app.put("/users/<id>")
def update_user(id: str):
    """
    Upadate the data of a particular user
    params: user id 
    returns: jsonified string saying updation successful
    """
    try:
        if not db.is_connected():
            return jsonify({
                "Message": "Database is not connected",
            }), 500
        
        # get the data from the user
        req = request.get_json()

        # query to accesse the unique data
        query_filter = {
            "_id": ObjectId(id), 
        }
    
        # properties to update
        update_operation = {
            "$set": {
                "name": req["name"],
                "username": req["username"],
                "password": req["password"],
            }
        }
        # update the data 
        db.users_collection.update_one(query_filter, update_operation)
        return jsonify({
            "Message":"Update successful"
        }), 200

    except Exception as e:
        return jsonify({
            "Message": str(e),
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
