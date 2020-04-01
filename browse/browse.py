from flask import Flask, render_template, request, redirect, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
import json
import os

browse = Flask(__name__)


browse.config['MONGO_URI'] = "mongodb://localhost:27017/travel_app"
browse.config['MONGO_DBNAME'] = "travel_app"
mongo = PyMongo(browse)
travel_app = mongo.db

@browse.route('/<uname>', methods=['GET','POST'])
def main(uname):
	uname = uname
	return render_template('webpage1.html', uname=uname)


@browse.route('/api/browse', methods=['GET', 'POST'])
def browse_api():
	places = travel_app["places"]
	province = request.args.get("province")
	print(province)
	places_fetch = places.find({"province":province})
	# for i in places_fetch:
	# 	print(i)
	# 	print("asonff")
	places_dict = {}
	counter=1
	for i in places_fetch:
		c = i.get('place_id')
		i['_id'] = c
		places_dict[c]=i
		counter+=1
	print(places_dict)
# return "oi"
	return jsonify(places_dict)


@browse.route('/destination', methods=['GET'])
def destination():
	return render_template('destination.html')
