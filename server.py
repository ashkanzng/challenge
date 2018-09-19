from flask import Flask
from flask import request
from order import orderClass
from flask import Response
import json

app = Flask(__name__)
@app.route("/order",methods=['POST'])
def order():
	postdata = request.get_json(force=True)
	orderObject = orderClass()
	validate = orderObject.setParametr(postdata)
	if validate["status"] != True:
		message={"error":validate["message"]}
		return Response(json.dumps(message), status=500, mimetype='application/json')
	result = orderObject.createOrder()
	return Response(json.dumps(result), status=200, mimetype='application/json')
	

@app.route("/order/<int:id>",methods=['PUT'])
def pickorder(id):
	postdata = request.get_json(force=True)
	orderObject = orderClass()
	out = orderObject.pickOrder(id)
	return Response(json.dumps(out), status=200, mimetype='application/json')


@app.route("/orders/<int:page>/<int:limit>",methods=['GET'])
def getAllOrders(page,limit):
	orderObject = orderClass()
	out = orderObject.getOrder(page,limit) 
	return json.dumps(out)


@app.route("/")
def index():
	return 'Index Pages'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080,debug = True, threaded=True)
