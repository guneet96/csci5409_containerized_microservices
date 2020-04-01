from flask import Flask, redirect, request, jsonify

import pymongo
#from flask_cognito import CognitoAuth
from flask_awscognito import AWSCognitoAuthentication
app = Flask(__name__)

app.config['AWS_DEFAULT_REGION'] = 'us-east-1'
app.config['AWS_COGNITO_DOMAIN'] = 'https://group16travelapp.auth.us-east-1.amazoncognito.com'
app.config['AWS_COGNITO_USER_POOL_ID'] = 'us-east-1_EVC4Db7P6'
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '2410gs4dlsf80inkirq73srbhm'
app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = 'roi5abh2rof35fbs94b52jetepn9apk0ddrfrtbjtpnmhlogfdt'
app.config['AWS_COGNITO_REDIRECT_URL'] = 'http://localhost:5003/aws_cognito_redirect'


aws_auth = AWSCognitoAuthentication(app)

@app.route('/')
@aws_auth.authentication_required
def index():
    claims = aws_auth.claims # or g.cognito_claims
    return jsonify({'claims': claims})

@app.route('/sign_in')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())

@app.route('/aws_cognito_redirect')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    return jsonify({'access_token': access_token})

if __name__ == '__main__':
    app.run(debug=True)