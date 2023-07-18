from flask import Flask,Response,request,make_response,jsonify
import pymongo
import json 
import jwt
from functools import wraps
from bson.objectid import ObjectId

app = Flask(__name__)
SECRET_KEY = '63a169ac0b6a437bb43ea81e0e12781b'


try:
    mongo = pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS = 1000)
    db=mongo.company
    mongo.server_info()
    

except:
    print("Error - cannot connect to db")


#############################################

@app.route("/register",methods=["POST"])
def Register():
    try:
        register = {
                'first_name' : request.json['first_name'],
                'last_name' :  request.json['last_name'],
                'email' :  request.json['email'],
                'password' :  request.json['password']
              }
        dbResponse = db.register.insert_one(register)
        
        print(dbResponse.inserted_id)
        #for x in dir(dbResponse):
        #    print(x)
        return Response(response=json.dumps({"message":"Registered Sucessfully","id":f"{dbResponse.inserted_id}"}),
                        status=200,
                        mimetype="application/json")
    except:
        pass
#############################################

@app.route("/login",methods=["POST"])
def login():
    try:
        login={'email' :  request.json['email'],
                'password' :  request.json['password']
            }
        user = db.register.find_one({'email': login['email']})
        if user and user['password'] == login['password']:
            jwt_token = SECRET_KEY
            return Response(response=json.dumps({"message": "Login successful", "token": jwt_token}), status=200, mimetype="application/json")

        # Create the JWT bearer token
        #    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        #    return Response(response=json.dumps({"message": "Login successful", "token": jwt_token}), status=200, mimetype="application/json")




            #return Response(response=json.dumps({"message":"Sucessfully logged in"}),
            #            status=200,
            #           mimetype="application/json")
            #token = jwt.encode({'email' :  request.json['email']},app.config['SECRET_KEY'])
            #return Response(response=json.dumps({"message":"Sucessfully logged in"),
            #        status=200,
            #        mimetype="application/json")  
                               
                               
        else:
            return "Wrong email and password"
    except:
        pass
########################################################################################

@app.route("/template",methods=["GET","POST"])
def insert_read():
    if request.method == "POST":
        try:
            insert={
            'template_name':request.json['template_name'],
            'subject':request.json['subject'],
            'body': request.json['body']
            }

            dbResponse = db.insert.insert_one(insert)
            return Response(response=json.dumps({"message":"Sucessfully inserted","id":f"{dbResponse.inserted_id}"}),
                        status=200,
                        mimetype="application/json")
        except:
           pass 
    elif request.method =="GET": 
        try:
            data=list(db.insert.find({}, {"_id": 0}))  
            return data
        except:
            pass

    else:
         pass


@app.route("/template/<string:_id>",methods=["GET","PUT","DELETE"])
def update_get_del(_id):
    if request.method == "GET":

        try:
            dbResponse = db.insert.find_one({"_id": ObjectId(_id)}, {"_id": 0})
            return dbResponse
            #if dbResponse:
                # Convert ObjectId to string before returning the response
                #dbResponse["_id"] = str(dbResponse["_id"])
                #return Response(response=json.dumps(dbResponse), status=200, mimetype="application/json")
            #else:
            #    return Response(response=json.dumps({"message": "Template not found"}), status=404, mimetype="application/json")
        except Exception as e:
            print(e)
            return Response(response=json.dumps({"message": "Error occurred while fetching template"}),
                            status=500, mimetype="application/json")
    
    elif request.method == "PUT":
        try:
            dbResponse = db.insert.update_one(
                {"_id": ObjectId(_id)},
                {"$set": {"template_name": request.json["template_name"], "subject": request.json["subject"], "body": request.json["body"]}}
            )

            if dbResponse.modified_count == 1:
                return Response(response=json.dumps({"message": "Template updated"}), status=200, mimetype="application/json")
            else:
                return Response(response=json.dumps({"message": "Template not found"}), status=404, mimetype="application/json")

        except Exception as e:
            print(e)
            return Response(response=json.dumps({"message": "Error occurred while updating template"}),
                            status=500, mimetype="application/json")
        
        
    elif request.method == "DELETE":
        try:
            # Use the delete_one() method to delete the document with the specified _id
            dbResponse = db.insert.delete_one({"_id": ObjectId(_id)})

            if dbResponse.deleted_count == 1:
                return Response(response=json.dumps({"message": "Template deleted"}), status=200, mimetype="application/json")
            else:
                return Response(response=json.dumps({"message": "Template not found"}), status=404, mimetype="application/json")

        except Exception as e:
            print(e)
            return Response(response=json.dumps({"message": "Error occurred while deleting template"}),
                            status=500, mimetype="application/json")
if __name__ == "__main__":
    app.run(port='0.0.0.0', debug=False)
