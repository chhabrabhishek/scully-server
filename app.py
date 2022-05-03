import json
from flask import Flask, request
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
def status():
    return "server is up and running ..."

@app.route("/get_transactions/<username>")
def get_transactions(username):
    data = {
        'query': 'query getTransactions($username: String){ transactions (where: {_or: [{transactionFrom: {_eq: $username}}, {transactionWith: {_eq: $username}}]} order_by: {transactionDate: desc, transactionId: desc}) { amount reason transactionDate transactionFrom transactionId transactionStatus transactionType transactionWith } }',
        'variables': { "username": username }
    }
    headers = {
        'content-type': 'application/json',
        'x-hasura-admin-secret': 'YlPkfjIaatJlBBPuo8ri3FgFs9UIg3hr1yNSUJNJXMlf4kx4uX3xItSszgq9EwHH'
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
        'x-hasura-admin-secret': 'YlPkfjIaatJlBBPuo8ri3FgFs9UIg3hr1yNSUJNJXMlf4kx4uX3xItSszgq9EwHH'
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
            'x-hasura-admin-secret': 'YlPkfjIaatJlBBPuo8ri3FgFs9UIg3hr1yNSUJNJXMlf4kx4uX3xItSszgq9EwHH'
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
            'query': 'query userExists ($username: String, $password: String) { users(where: {_and: [{username: {_eq: $username}}, {password: {_eq: $password}}]}) { balance } }',
            'variables': { "username": request_params['username'], "password": request_params['password'] }
        }
        headers = {
            'content-type': 'application/json',
            'x-hasura-admin-secret': 'YlPkfjIaatJlBBPuo8ri3FgFs9UIg3hr1yNSUJNJXMlf4kx4uX3xItSszgq9EwHH'
        }
        req = requests.post('https://scully.hasura.app/v1/graphql', data=json.dumps(data), headers=headers)
        data = req.json()
        if len(data['data']['users']):
            return {'userExists': True, 'balance': data['data']['users'][0]['balance']}
        else :
            return {'userExists': False}

@app.route("/get_users")
def get_users():
    try:
        data = {
            'query': 'query { users { username } }'
        }
        headers = {
            'content-type': 'application/json',
            'x-hasura-admin-secret': 'YlPkfjIaatJlBBPuo8ri3FgFs9UIg3hr1yNSUJNJXMlf4kx4uX3xItSszgq9EwHH'
        }
        req = requests.post('https://scully.hasura.app/v1/graphql', data=json.dumps(data), headers=headers)
        print(req)
        print(req.json())
        print(req.status_code)
        return req.json()
    except Exception as e:
        print(e)
        return "error arose"

@app.route("/add_transaction", methods=['POST', 'GET'])
def add_transaction():
    if request.method == 'POST':
        request_params = request.get_json()
        data = {
            'query': 'mutation addTransaction($transactionType: String, $transactionDate: date, $transactionStatus: String, $transactionFrom: String, $transactionWith: String, $reason: String, $amount: Int) { insert_transactions_one(object: {amount: $amount, reason: $reason, transactionDate: $transactionDate, transactionFrom: $transactionFrom, transactionStatus: $transactionStatus, transactionType: $transactionType, transactionWith: $transactionWith}){ transactionId } }',
            'variables': { "transactionType": request_params['transactionType'], "transactionDate": request_params['transactionDate'], "transactionStatus": "unpaid", "transactionFrom": request_params['transactionFrom'], "transactionWith": request_params['transactionWith'], "reason": request_params['reason'], "amount": request_params['amount'] }
        }
        headers = {
            'content-type': 'application/json',
            'x-hasura-admin-secret': 'YlPkfjIaatJlBBPuo8ri3FgFs9UIg3hr1yNSUJNJXMlf4kx4uX3xItSszgq9EwHH'
        }
        req = requests.post('https://scully.hasura.app/v1/graphql', data=json.dumps(data), headers=headers)
        return req.json()
