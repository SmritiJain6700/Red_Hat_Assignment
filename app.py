import json
import bson.errors
import pika
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, make_response
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/pizza_house"
mongo = PyMongo(app)


# Welcome API
@app.route('/welcome', methods=['GET'])
def welcome():
    message = "Welcome to Pizza House"
    return jsonify(message)


'''
# Store the order in db
@app.route('/order', methods=['POST'])
def acceptOrder():
    __json = request.json
    __order = __json['orders']
    if request.method == 'POST':
        idOrder = mongo.db.orders.insert_one({'orders': __order}).inserted_id
        resp = jsonify("Order added successfully")
        resp.status_code = 200
        orderId = jsonify({"orderId": str(idOrder), "status": resp.status_code})
        return orderId
    else:
        return notFound()
'''


# Get all order details
@app.route('/getorders', methods=['GET'])
def getAllOrders():
    orders = mongo.db.orders.find()
    response = json.loads(dumps(orders))
    return response


# Get order detail by order id
@app.route('/getorders/<orderid>', methods=['GET'])
def getOrderOfOrderId(orderid):
    try:
        orders = mongo.db.orders.find_one({'_id': ObjectId(orderid)})
        response = json.loads(dumps(orders))
        return response
    except bson.errors.InvalidId:
        return notFound()


# Enqueuing API requests using rabbitmq
@app.route('/order', methods=['POST'])
def order():
    order_details = request.json
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='saveOrder')
    channel.basic_publish(exchange='',
                          routing_key='saveOrder',
                          body=str(order_details))  # sending the order to the message queue
    connection.close()
    return make_response(jsonify("Order Placed!"), 201)


@app.errorhandler(404)
def notFound(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(debug=True)
