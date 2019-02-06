from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.aNewDB
UserNum = db["UserNum"]
UserNum.insert(
    {
        'num_of_users':0
    }
)

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_number = prev_num + 1
        UserNum.update({}, {"$set":{'num_of_users':new_number}}) #set requires " " here
        return str("Hello user " + str(new_number))

def checkPostedData(postedData, functionName):
    if functionName == "add":
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200

class Add(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "add")

        if status_code != 200:
            retJson = {
                "Nessage": "An error happened",
                "status": 200
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)



        ret = x+y
        retMap = {
            "Sum": ret,
            "status code": 200
        }
        return jsonify(retMap)

class Subtrract(Resource):
    pass

class Multiply(Resource):
    pass

class Divide(Resource):
    pass


api.add_resource(Add, "/add")
api.add_resource(Visit, "/hello")

bye = {
    'App': 'nice',
    'age': 4
}

@app.route('/')
def hello_world():
    return "Hello World!"

# @app.route('/bye')
# def bye_func():
#     return jsonify(bye)

# @app.route('/add_two_nums', methods=["POST", "GET"])
# def add():
#     data = request.get_json()
#     x = data["x"]
#     y = data["y"]

#     z=x+y

#     retJSON={
#         "z":z
#     }
#     return jsonify(retJSON)

if __name__=="__main__":
    app.run(host='0.0.0.0')