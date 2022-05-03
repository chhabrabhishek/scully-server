import json
from flask import Flask
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