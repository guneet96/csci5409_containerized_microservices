from flask import Flask, render_template, request, redirect, jsonify
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
import json
import os
import pprint


flight = Flask(__name__)
api = Api(flight)

flight.config['MONGO_URI'] = "mongodb://localhost:27017/p_db"
flight.config['MONGO_DBNAME'] = "p_db"
mongo = PyMongo(flight)
travel_app = mongo.db


@flight.route('/flight', methods=['GET'])
def main():
	return render_template('flights.html')
	flights = travel_app["flights"]
	flight_fetch = flights.find()
	flight_dic = {}
	counter=1
	for i in flight_fetch:
		c = i.get('code')
		i['_id'] = counter
		flight_dic[c]=i
		counter+=1

	# return "oi"
	return jsonify(flight_dic)


@flight.route('/api/flight', methods=['GET','POST'])
def api_flights():
	source = request.args.get("source")
	destination = request.args.get("destination")
	flight = travel_app["flight"]
	flight_query_fetch = flight.find({"source":source,"destination":destination})
	# , "destination":destination})
	# for i in flight_query_fetch:
	# 	print(i)

	flight_dic = {}
	counter=1
	for i in flight_query_fetch:
		c = i.get('code')
		# print("Hi")
		i['_id'] = c
		# print(c)
		flight_dic[c]=i
		counter+=1
	# print(counter)
	# print(flight_dic)
	# return "oi"
	return jsonify(flight_dic)


# class FlightList(Resource):



if __name__== "__main__":
	flight.run(debug=True)