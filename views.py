import os, re;
import requests
from flask import Flask, jsonify, request, Response, render_template
from faker import Factory
from twilio.util import TwilioCapability
import twilio.twiml
import models

app = Flask(__name__)
fake = Factory.create()
alphanumeric_only = re.compile('[\W_]+')
phone_pattern = re.compile(r"^[\d\+\-\(\) ]+$")

default_reps = models.states['ny']

@app.route('/')
def index():
    return render_template(
        'index.html',
        reps=default_reps
    )

@app.route('/state/<name>')
def state(name):
    state_name = name.lower()
    reps = models.states[state_name] if state_name in models.states else default_reps
    return render_template(
        'index.html',
        reps=reps
    )

@app.route('/token', methods=['GET'])
def token():
    # get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    application_sid = os.environ['TWILIO_TWIML_APP_SID']
    
    # Generate a random user name
    identity = alphanumeric_only.sub('', fake.user_name())

    # Create a Capability Token
    capability = TwilioCapability(account_sid, auth_token)
    capability.allow_client_outgoing(application_sid)
    capability.allow_client_incoming(identity)
    token = capability.generate()

    # Return token info as JSON
    return jsonify(identity=identity, token=token)

    
@app.route("/voice", methods=['POST'])
def voice():
    resp = twilio.twiml.Response()
    if models.clean_phone(request.form["To"]) not in models.phones:
        resp.say("Incorrect phone number")
    else:
        if "To" in request.form and request.form["To"] != '':
            dial = resp.dial(callerId=os.environ['TWILIO_CALLER_ID'])
            # wrap the phone number or client name in the appropriate TwiML verb
            # by checking if the number given has only digits and format symbols
            if phone_pattern.match(request.form["To"]):
                dial.number(request.form["To"])
            else:
                dial.client(request.form["To"])
        else:
            resp.say("Thanks for calling!")
    return Response(str(resp), mimetype='text/xml')


if __name__ == '__main__':
    app.run()