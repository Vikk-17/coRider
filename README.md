# coRider

**Tested in linux environment (Arch btw)**

## Introduction
A Flask application that performs CRUD (Create, Read, Update, Delete) operations on a MongoDB database for a User resource using a REST API. The REST API endpoints should be accessible via HTTP requests and tested using Postman.

## Prerequisites
Before start make sure that the following things are installed:
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Postman](https://www.postman.com/)


## Local setup

Clone the repository into the local machine
```bash
git clone https://github.com/Vikk-17/coRider.git
cd coRider
```

Create a virtual environment in the root directory
```bash
python -m venv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Install all the dependecies
```bash
pip install -r requirements.txt
```

Run the application
```bash
python main.py
```

## Containerization

### Build the image
Go to the top level directory of the project, and run the following command
```bash
docker build -t <image_name:tag_name> .

// Example
docker build -t nervous_torvalds:latest .
```

### Create and run the container

Now run the following command to create and run the docker container:
```bash
docker run -p <HostPort:ContainerPort> -e MONGO_URI="MongoDB-connection-string" <image_name>

// Example
docker run -p 3000:3000 -e MONGO_URI="mongodb+srv://admin:admin123@cluster0.r0k4t.mongodb.net/" nervous_torvalds
```
- `-e`: To provide environment variable
- `-p`: To map port of host to container

### Test the container
Now run the postman and send requests to endpoints.


## API Endpoints
- `GET /users` - Returns a list of all users.
- `GET /users/<id>` - Returns the user with the specified ID.
- `POST /users` - Creates a new user with the specified data.
- `PUT /users/<id>` - Updates the user with the specified ID with the new data.
- `DELETE /users/<id>` - Deletes the user with the specified ID.



## Screenshots
![Docker Container](./assests/docker.png)
![Get Users](./assests/get_users.png)
![Get Specific User](./assests/get_spcecifi_user.png)
![Delete User Details](./assests/delete_user_details.png)
![Delete User Status](./assests/delete_user_status.png)
![Update User Data](./assests/update_user_data.png)
![Update User Status](./assests/update_status.png)
![Change of Data](./assests/update_data_change.png)
