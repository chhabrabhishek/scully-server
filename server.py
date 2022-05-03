import json
from flask import Flask, request
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/get_transactions/<username>")
def get_transactions(username):
    data = {
        'query': 'query getTransactions($username: String){ transactions (where: {_or: [{transactionFrom: {_eq: $username}}, {transactionWith: {_eq: $username}}]}) { money reason transactionDate transactionFrom transactionId transactionStatus transactionType transactionWith } }',
        'variables': { "username": username }
    }
    headers = {
        'content-type': 'application/json',
        'x-hasura-admin-secret': '5llFpm8mZWkMvp620CMzMbyfNKSq2VxV5bXjOOABjOO9IhiCaYKrYeFXeiIMq9ea'
    }
    req = requests.post('https://scully.hasura.app/v1/graphql', data=json.dumps(data), headers=headers)
    return req.json()

@app.route("/mark_paid/<transactionId>")
def mark_paid(transactionId):
    data = {
        'query': 'mutation markAsPaid($transactionId: Int) { update_transactions(_set: {transactionStatus: "paid"} where: {transactionId:{_eq: $transactionId}}){ affected_rows } }',
        'variables': { "transactionId": transactionId }
    }
    headers = {
        'content-type': 'application/json',
        'x-hasura-admin-secret': '5llFpm8mZWkMvp620CMzMbyfNKSq2VxV5bXjOOABjOO9IhiCaYKrYeFXeiIMq9ea'
    }
    req = requests.post('https://scully.hasura.app/v1/graphql', data=json.dumps(data), headers=headers)
    return req.json()

@app.route("/user_sign_up", methods=['POST', 'GET'])
def username_exists():
    if request.method == 'POST':
        request_params = request.get_json()
        data = {
            'query': 'mutation addUser($username: String, $password: String, $balance: Int) { insert_users_one(object: {username: $username, password: $password, balance: $balance}) { username } }',
            'variables': { "username": request_params['username'], "password": request_params['password'], "balance": request_params['balance'] }
        }
        headers = {
            'content-type': 'application/json',
            'x-hasura-admin-secret': '5llFpm8mZWkMvp620CMzMbyfNKSq2VxV5bXjOOABjOO9IhiCaYKrYeFXeiIMq9ea'
        }
        req = requests.post('https://scully.hasura.app/v1/graphql', data=json.dumps(data), headers=headers)
        data = req.json()
        if 'errors' in data:
            return {'usernameExists': True}
        else :
            return {'userAdded': True}

@app.route("/user_login", methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        request_params = request.get_json()
        data = {
            'query': 'query userExists ($username: String, $password: String) { users(where: {_and: [{username: {_eq: $username}}, {password: {_eq: $password}}]}) { username } }',
            'variables': { "username": request_params['username'], "password": request_params['password'] }
        }
        headers = {
            'content-type': 'application/json',
            'x-hasura-admin-secret': '5llFpm8mZWkMvp620CMzMbyfNKSq2VxV5bXjOOABjOO9IhiCaYKrYeFXeiIMq9ea'
        }
        req = requests.post('https://scully.hasura.app/v1/graphql', data=json.dumps(data), headers=headers)
        data = req.json()
        if len(data['data']['users']):
            return {'userExists': True}
        else :
            return {'userExists': False}
