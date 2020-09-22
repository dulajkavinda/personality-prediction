# app.py
import os
from flask_cors import CORS
from difflib import SequenceMatcher
from flask import Flask, request, jsonify
app = Flask(__name__)
CORS(app)
from sklearn.externals import joblib
from flask_restful import reqparse
from bson.json_util import dumps
from flask_pymongo import PyMongo
from pymongo import MongoClient
app.config["MONGO_URI"] = "mongodb+srv://dulaj:12345@cluster0-jtd1d.mongodb.net/personality?retryWrites=true&w=majority"

mongo = PyMongo(app)
db = mongo.db
col = mongo.db["test"]
print ("MongoDB Database:", mongo.db)



parse = reqparse.RequestParser()

model = joblib.load('model.pkl')
prediction = model.predict([[9,1,9,3,4,5,9]])[0]
print(prediction)

@app.route('/getJobs', methods=['GET'])
def getJobs():
    myresults = list(db.jobs.find())
    print(myresults)
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return  json_data


@app.route('/predict', methods=['POST'])
def respond():
    request_json = request.get_json()

    parm1 = request_json.get('age')
    parm2 = request_json.get('gender')
    parm3 = request_json.get('openness')
    parm4 = request_json.get('neuroticism')
    parm5 = request_json.get('conscientiousness')
    parm6 = request_json.get('agreeableness')
    parm7 = request_json.get('extraversion')

    parm1 = int(parm1)
    parm2 = int(parm2)
    parm3 = int(parm3)
    parm4 = int(parm4)
    parm5 = int(parm5)
    parm6 = int(parm6)
    parm7 = int(parm7)

    prediction = model.predict([[parm1, parm2, parm3, parm4,parm5, parm6, parm7]])[0]

    return jsonify({
        'Prediction': prediction
    })

@app.route('/addcandidate', methods=['POST'])
def addcandidate():
    request_json = request.get_json()

    vehicancy_id = request_json.get('vehicancy_id')
    Id = request_json.get('Id')
    job = request_json.get('job')
    applicants_name = request_json.get('applicants_name')
    age = request_json.get('age')
    bio = request_json.get('bio')
    email = request_json.get('email')
    cv_text = request_json.get('cv_text')
    gender = request_json.get('gender')
    openness = request_json.get('openness')
    neuroticism = request_json.get('neuroticism')
    conscientiousness = request_json.get('conscientiousness')
    agreeableness = request_json.get('agreeableness')
    extraversion = request_json.get('extraversion')
    cv_name = request_json.get('cv_name')
    per = request_json.get('per')

    candidate = {'vehicancy_id': vehicancy_id, 'job': job, 'applicants_name': applicants_name, 'age': age,'email': email, 'cv_text': cv_text, 'gender': gender
                 , 'openness': openness, 'neuroticism': neuroticism,'conscientiousness': conscientiousness, 'agreeableness': agreeableness, 'extraversion': extraversion,'bio':bio, 'cv_name':cv_name,'per':per,
                 'Id':Id}
    db.candidates.insert_one(candidate)
    response =  jsonify({
        'Status': 'Done'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route('/addjob', methods=['POST'])
def addjob():
    request_json = request.get_json()

    Id = request_json.get('Id')
    company = request_json.get('company')
    experience = request_json.get('experience')
    education = request_json.get('education')
    title = request_json.get('title')
    job_desc = request_json.get('job_desc')

    candidate = {'Id': Id, 'company': company, 'experience': experience, 'education': education,'job_desc': job_desc,'title':title}
    db.jobs.insert_one(candidate)
    response =  jsonify({
        'Status': 'Done'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/candidateCount', methods=['POST'])
def findsCandidateCount():
    request_json = request.get_json()

    Id = request_json.get('Id')

    myresults = list(db.jobs.find({'Id': Id}))
    print(myresults)
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return json_data

@app.route('/updateCandidateCount', methods=['POST'])
def updateCandidateCount():
    request_json = request.get_json()

    Id = request_json.get('Id')

    myresults = list(db.jobs.find_one_and_update( {'Id': Id}, {'$inc': {'candidates': 1}}))
    print(myresults)
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return json_data

@app.route('/findCandidates', methods=['POST'])
def findCandidates():
    request_json = request.get_json()

    Id = request_json.get('Id')

    myresults = list(db.candidates.find({'vehicancy_id': Id}))
    print(myresults)
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return json_data

@app.route('/updatePrediction', methods=['POST'])
def updatePrediction():
    request_json = request.get_json()

    Id = request_json.get('Id')
    per = request_json.get('per')

    myresults = list(db.candidates.find_one_and_update( {'Id': Id}, {'$set': {'per': per}}))
    print(myresults)
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return json_data

@app.route('/updateScore', methods=['POST'])
def updateScore():
    request_json = request.get_json()

    Id = request_json.get('Id')
    score = request_json.get('score')

    myresults = list(db.candidates.find_one_and_update( {'Id': Id}, {'$set': {'score': score}}))
    print(myresults)
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return json_data

@app.route('/getcandidate', methods=['POST'])
def getCandidate():
    request_json = request.get_json()

    Id = request_json.get('Id')

    myresults = list(db.candidates.find({'Id': Id}))
    print(myresults)
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return json_data

@app.route('/uploadCV', methods=['POST'])
def uploadCV():
    cv_pdf = request.files['file']
    mongo.save_file(cv_pdf.filename, cv_pdf)
    return "Done"

@app.route('/file/<filename>')
def getCV(filename):
    return mongo.send_file(filename)

@app.route('/getSimilarity', methods=['POST'])
def getSimilarity():
    request_json = request.get_json()

    first_text = request_json.get('ftext')
    second_text = request_json.get('stext')
    myresults = SequenceMatcher(None, first_text,second_text).ratio()
    # Converting to the JSON
    json_data = dumps(myresults, indent=2)
    return  json_data


@app.route('/')
def index():
    title = 1
    priority = 1
    shortdesc = 1
    task_id = 1
    task = {'id': task_id, 'title': title, 'shortdesc': shortdesc, 'priority': priority}

    db.cclecture.insert_one(task)
    return "<h1>Welcome to Iris Prediction server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)