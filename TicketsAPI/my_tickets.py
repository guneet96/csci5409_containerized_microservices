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


#get booking details of particular user
@app.route('/get/<email>')
def user(email):
	user = collection.find_one({'email_id':email},{'_id': False})
	resp = {}
	if(user):
		resp['message'] = "User found"
		resp['user'] = user
	else:
		resp['message'] = "User not found"
	resp['status_code'] = 200
	return resp

#get pdf for particular booking for particular user
@app.route('/getPdf',methods=['POST'])
def getPdf():
	_json = request.get_json()
	print(_json);
	_email_id = _json['email_id']
	_booking_no = _json['booking_no']

	user = collection.find_one({'email_id':_email_id})
	bookings = user['bookings']
	selected_booking = {}
	selected_flight_details = {}
	selected_tarvellername = []
	found = False
	for booking in bookings:
		if booking['booking_no'] == _booking_no:
			found = True
			selected_booking = booking
			break
	selected_flight_details = selected_booking['flight_details']
	selected_tarvellername = selected_booking['traveller_name']

	rendered = render_template('pdf_template.html',email_id=_email_id,booking_no=_booking_no,date_time=selected_booking['date_time'],departure_plc=selected_flight_details['departure_plc'],destination_plc=selected_flight_details['destination_plc'],departure_date=selected_flight_details['departure_date'],flight_name=selected_flight_details['flight_name'],departure_time=selected_flight_details['departure_time'],total_hour=selected_flight_details['total_hour'],destination_time=selected_flight_details['destination_time'],destination_date=selected_flight_details['destination_date'],data=enumerate(selected_tarvellername),price=selected_flight_details['price'],amount=selected_booking['amount'])
	config = pdfkit.configuration(wkhtmltopdf="E:\\pdfkit\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
	pdf = pdfkit.from_string(rendered, False, configuration=config)

	response = make_response(pdf)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

	return response

@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status':404,
		'message':'Not Found '+request.url
		}
	resp = jsonify(message)
	resp.status_code =  404
	return resp 


if __name__ == "__main__":
	app.run(debug=True)