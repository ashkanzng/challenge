import re
import mysql.connector
from time import sleep 
import time
import requests as httprequest
import datetime
from conf import *


class orderClass(object):

	""" status    = 0 			     Default is 0 means None Taken,  1=> Is taken
		googleApi = GoogleAPIkey     Import from conf file
	"""

	def __init__(self):
		self.connection = mysql.connector.connect(user='root', password='admin',host='mysql_server_container',port='3306',database='orders')
		self.origin_lat = None
		self.origin_lon = None 
		self.destination_lat = None
		self.destination_lon = None
		self.status = 0 
		self.googleApi = GoogleAPIkey 

	""" Method getDistance from google api """
	def getDistance(self):
		URL = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
		googleLatLon = {
				'origins':self.origin_lat+","+self.origin_lon,
				"destinations":self.destination_lat+","+self.destination_lon,
				"key":self.googleApi
			} 
		r = httprequest.get(url = URL, params = googleLatLon) 
		try:
			out = r.json()["rows"][0]["elements"][0]["distance"]["value"]
		except Exception as e:
			out = 0
		return str(out)

	""" validatePrametr Check valid number for lat and long ;param str """
	def validatePrametr(self,param):
		number = re.search('^(?=.?\d)\d*[.,]?\d*$', param, re.IGNORECASE)
		if number is None:
			raise ValueError('number required (string given)' + param)
		return param

	""" Method set class entity  ;parametr dic """
	def setParametr(self,parametr):
		errorCheck={"status":True,"message":"prametr passed :)"}
		try:
			self.origin_lat = self.validatePrametr(parametr["origin"][0])
			self.origin_lon = self.validatePrametr(parametr["origin"][1])
			self.destination_lat = self.validatePrametr(parametr["destination"][0])
			self.destination_lon = self.validatePrametr(parametr["destination"][1])
			return errorCheck
		except Exception as e:
			return {"status":False,"message":"rametr ERROR :( " + str(e)}





	""" Method createOrder """
	def createOrder(self):
		out = self.insertOrder()
		return out

	""" Method getOrder with offset and limit ;page int, limit int"""
	def getOrder(self,page,limit):
		offset = 0
		if int(page) > 1:
			offset = 5*int(page)
		out = self.selectOrders(offset,limit)
		return out

	""" Method getOrder with offset and limit ;orderid int"""
	def pickOrder(self,orderid):
		findOrder = self.findOrders(orderid)
		if findOrder:
			if findOrder[1] ==0:
				return self.updateOrder(orderid)
			return {"error": "ORDER_ALREADY_BEEN_TAKEN"}	
		return {"error": "ORDER_NOT_EXIST"}
			


	""" Method insert Order that insert row in mysql """
	def insertOrder(self):
		output={"id":None,"distance":None,"status":"UNASSIGN"}
		distance = self.getDistance()
		output["distance"] = distance
		print distance
		createdate = time.time()
		cursor = self.connection.cursor()
		
		query = ("""INSERT INTO order_requests 
			(`origin_lat`,`origin_lon`,`destination_lat`,`destination_lon`,`distance`,`createdate`,`status`) VALUES 
			(%s, %s, %s, %s, %s, %s, %s)  """)

		cursor.execute(query,(self.origin_lat,self.origin_lon,self.destination_lat,self.destination_lon,distance,createdate,self.status,))
		self.connection.commit()
		output["id"] = str(cursor.lastrowid) 
		output["status"] = "UNASSIGN" 
		cursor.close()
		return output

	""" Method select Order from mysql """
	def selectOrders(self,offset,limit): 
		output=[]
		cursor = self.connection.cursor()
		query = (""" SELECT id,distance,status FROM order_requests limit %s,%s """)
		cursor.execute(query,(int(offset),int(limit),))
		rows = cursor.fetchall()
		cursor.close()
		for row in rows:
			output.append({"id":row[0],"distance":row[1],"status":row[2]})
		return output

	""" Method find Order from mysql by id """
	def findOrders(self,orderid): 
		cursor = self.connection.cursor()
		query = (""" SELECT id,status FROM order_requests WHERE id = %s  """)
		cursor.execute(query,(orderid,))
		row = cursor.fetchone()
		cursor.close()
		return row
		

	""" Method update Order in mysql """
	def updateOrder(self,orderid):
		cursor = self.connection.cursor()
		query = ("""UPDATE order_requests SET `status`= 1 WHERE id = %s """)
		cursor.execute(query,(orderid,))
		self.connection.commit()
		cursor.close()
		return {"status": "SUCCESS"}

	""" Method Close connection to database """
	def CloseConnectionDatabase(self):
		self.connection.close()






