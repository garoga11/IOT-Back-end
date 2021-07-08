from flask import Flask, json, jsonify, request
from flask_restful import Api, Resource, abort
from flask_cors import CORS
import db_config as database
import hashlib, uuid
from hashlib import blake2b
from datetime import datetime
from bson import json_util

app = Flask(__name__)


@app.route('/login/', methods=['GET'])
def get():
    user_id = str(request.args.get("user_id"))
    money = int(request.args.get("money"))
    token = request.args.get("abc")
    
    # print(token+" ARDUINO")
    # hola = "hola"
    # hola = blake2b(digest_size=10).hexdigest()
    # print(hola)

    key = f"Hi9@yBl4$j8WM91*4Wf8{user_id}{money}"
    # key_hash= hashlib.sha256(str(key).encode('utf-8'))
    # key_str= str(key_hash)
 
    key_str= str(key)

    key_str = blake2b(digest_size=64).hexdigest()
    # token = blake2b(digest_size=64).hexdigest()

    print(key_str)
    print(token)
    # key_h="hola"

    if token == key_str:
        _request= database.db.passenger_transactions.find_one({"_id":user_id})

        if _request:
            
            current_balance = _request["current_balance"]
            
            date=datetime.now()
            transaction_id = uuid.uuid1()
            date_str =date.strftime('%d/%m/%Y')

            new_transaction = database.db.passenger_transactions.update_one({"_id": user_id}, {"$push":{
            "transactions":{
                "id": transaction_id,
                "date": date_str,
                "amount": money
            }}})

            if new_transaction:
                money_int= int(money)
                final_balance= current_balance+ money_int
                balance_update=database.db.passenger_transactions.update_one({'_id':user_id},
                {'$set':{ 
                    'current_balance': final_balance
                }})

                if balance_update:
                    return jsonify({"message":"successful transaction"})
                else:
                    return jsonify({"message":"Balance could't be updated"})
            else: 
                return jsonify({"message":"Unsuccessful transaction"})
        else:
            return jsonify({"message":"Invalid userId"})
    else:
        return jsonify({"message":"Invalid token"})


if __name__ == '__main__':
    app.run(debug=True)