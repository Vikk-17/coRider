# coRider

**The code is tested in linux environment only**

## Introduction
A Flask application that performs CRUD (Create, Read, Update, Delete) operations on a MongoDB database for a User resource using a REST API. The REST API endpoints should be accessible via HTTP requests and tested using Postman.

## Prerequisites
Before start make sure that the following things are installed:
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)


## Local setup

Clone the repository into the local machine
```
git clone https://github.com/Vikk-17/coRider.git
```

Install all the dependecies
```
pip install -r requirements.txt
```

Run the application
```
python main.py
```

## Containerization

### Build the image
Go to the top level directory of the project, and run the following command
```
docker build -t <name:tag_name> .

// Example
docker build -t nervous_torvalds:latest .
```

### Create and run the container

Now run the following command to create and run the docker container:
```
docker run -p 3000:3000 -e MONGO_URI="MongoDB-connection-string" <name>

// Example
docker run -p 3000:3000 -e MONGO_URI="mongodb+srv://admin:admin123@cluster0.r0k4t.mongodb.net/" nervous_torvalds
```



