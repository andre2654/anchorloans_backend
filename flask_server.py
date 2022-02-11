from flask import Flask
from flask import request
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import json
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values(".env")
CONNECTION_STRING = config['CONNECTION_STRING']


@app.route("/user/add", methods=['POST'])
def add_user():
    client = MongoClient(CONNECTION_STRING)
    mydb = client["anchorloans"]
    mycol = mydb["users"]

    name = request.get_json()['name']
    password = request.get_json()['password']
    admin = request.get_json()['admin']

    myquery = {"name": name}

    response = mycol.find_one(myquery)

    if (json.loads(json_util.dumps(response)) != None):
        return {'message': 'User already registered'}

    mydict = {"name": name, "password": password, "admin": admin}

    response = mycol.insert_one(mydict)

    return {'message': 'ok'}


@app.route("/user/view", methods=['GET'])
def view_user():
    client = MongoClient(CONNECTION_STRING)
    mydb = client["anchorloans"]
    mycol = mydb["users"]

    name = request.args.get('name')
    password = request.args.get('password')

    user = {"name": name, "password": password}

    response = mycol.find_one(user)

    return {'response': json.loads(json_util.dumps(response))}


@app.route("/img/add", methods=['POST'])
def add_img():
    client = MongoClient(CONNECTION_STRING)
    mydb = client["anchorloans"]
    mycol = mydb["imgs"]

    uploadedBy = request.get_json()['uploadedBy']
    fileURL = request.get_json()['fileURL']
    approvedStatus = request.get_json()['approvedStatus']

    mydict = {"uploadedBy": uploadedBy, "fileURL": fileURL,
              "approvedStatus": approvedStatus}

    response = mycol.insert_one(mydict)

    return {'message': 'ok'}


@app.route("/img/view", methods=['GET'])
def view_imgs():
    client = MongoClient(CONNECTION_STRING)
    mydb = client["anchorloans"]
    mycol = mydb["imgs"]

    response = mycol.find()

    return {'response': json.loads(json_util.dumps(response))}


@app.route("/img/approve", methods=['POST'])
def approve_img():
    client = MongoClient(CONNECTION_STRING)
    mydb = client["anchorloans"]
    mycol = mydb["imgs"]

    id = request.get_json()['id']

    myquery = {"_id": ObjectId(id)}
    uploadquery = {"$set": {"approvedStatus": True}}

    response = mycol.update_one(myquery, uploadquery)

    return {'message': 'ok'}


@app.route("/img/rejected", methods=['POST'])
def rejected_img():
    client = MongoClient(CONNECTION_STRING)
    mydb = client["anchorloans"]
    mycol = mydb["imgs"]

    id = request.get_json()['id']

    myquery = {"_id": ObjectId(id)}

    response = mycol.delete_one(myquery)

    return {'message': 'ok'}


if __name__ == "__main__":
    app.run(debug=True)
