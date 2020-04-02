from bson.json_util import dumps
from flask import Flask, jsonify, request, render_template, make_response
import pdfkit
from pymongo import MongoClient
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import uuid
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = "secretkey"


client = MongoClient(port=27017)
db = client['project'];
collection = db['Bookings'];

# get,delete,add

@app.route('/add',methods=['POST'])
def add_booking():
	_json = request.get_json()
	
	_email_id = _json['email_id']

	bookings = [];
	for booking in _json['bookings']:
		booking_dict = {}
		booking_dict['booking_no'] = generateUniqueId();
		booking_dict['date_time'] = str(datetime.now()).split('.')[0]

		traveller_names = []
		for traveller_name in booking['traveller_name']:
			traveller_name_dict = {}
			traveller_name_dict['fname'] = traveller_name['fname']
			traveller_name_dict['lname'] = traveller_name['lname']
			traveller_names.append(traveller_name_dict)
	
	booking_dict['traveller_name'] = traveller_names
	booking_dict['amount'] = booking['amount']
	flight_details_dict = {}

	flight_details = booking['flight_details']
	flight_details_dict['flight_logo'] = flight_details['flight_logo']
	flight_details_dict['flight_name'] = flight_details['flight_name']
	flight_details_dict['departure_plc'] = flight_details['departure_plc']
	flight_details_dict['destination_plc'] = flight_details['destination_plc']
	flight_details_dict['departure_time'] = flight_details['departure_time']
	flight_details_dict['departure_date'] = flight_details['destination_date']
	flight_details_dict['destination_time'] = flight_details['destination_time']
	flight_details_dict['destination_date'] = flight_details['destination_date']
	flight_details_dict['pls_day'] = flight_details['pls_day']
	flight_details_dict['total_hour'] = flight_details['total_hour']
	flight_details_dict['no_stops'] = flight_details['no_stops']
	flight_details_dict['price'] = flight_details['price']
	booking_dict['flight_details'] = flight_details_dict

	bookings.append(booking_dict);

	user = collection.find_one({'email_id':_email_id})

	new = False
	if(user):
		new = False;
		user['bookings'].append(bookings)
		collection.update_one({'email_id':_email_id},{'$set':user})
	else:
		new = True
		user = {};
		user['email_id'] = _email_id
		user['bookings'] = bookings 
		collection.insert(user)

	# resp = jsonify(str(new)+" Ticket booked successfully")
	resp = {};
	resp['message'] = str(new)+" Ticket booked successfully"
	resp['status_code'] = 200
	return resp


def generateUniqueId():
	dta = str(datetime.now()).split('.')[0].split(' ')
	part1 = ''.join(dta[0].split('-'))
	part = part1 + ''.join(dta[1].split(':'))
	part = part[2:]
	return str(ObjectId(bytes(part,'utf-8')))


if __name__ == "__main__":
	app.run(debug=True)