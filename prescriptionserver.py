import json
from flask import Flask, request, redirect, Response, json
import requests
import io
import time
import datetime
import sys
import os
import json
import subprocess
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Attachment
import base64
from google.cloud import storage
##from twilio.twiml.voice_response import Record, VoiceResponse, Say
##from twilio.twiml.messaging_response import MessagingResponse
##from google.cloud import speech
##from google.cloud.speech import enums
##from google.cloud.speech import types
##from google.cloud import translate
##from twilio.twiml.voice_response import VoiceResponse
from flask_cors import CORS
import pdfkit
from twilio.rest import Client
import requests
import pymongo
from pymongo import MongoClient
import pyqrcode 
from pyqrcode import QRCode 
from bson.json_util import dumps

cluster = MongoClient("MONGO STRING URI HERE")
db = cluster["remotepharmacy"]
db2 = cluster["radose"]

currpresid = 30

app = Flask(__name__)
CORS(app)

def send_sms(number):
    with open('swamphackscredentials.json', 'r') as f:
        creds = json.load(f)


    account_sid = creds["twilio"]["account_sid"]
    auth_token  = creds["twilio"]["auth_token"]
    sender = creds["twilio"]["sender"]

    ##print (account_sid)
    ##print (auth_token)

    client = Client(account_sid, auth_token) 

    ##sender = sys.argv[1]
    receiver = number
    text = "Thank you for using our system "



    message = client.messages.create( 
                                  from_=sender,  
                                  body=text,      
                                  to=receiver 
                              )



    print(message.sid)


def send_email(usermail):
    with open('credentials.json', 'r') as f:
        creds = json.load(f)


    sendgridapikey = creds["sendgrid"]["api_key"]

    sg = sendgrid.SendGridAPIClient(apikey=sendgridapikey)

    ##usermail = sys.argv[1]

    from_email = Email("PharmaNotifier@remotepharmacyai.com")
    subject = "WeFundGov donation"
    ##to_email = Email("jemsbhai@gmail.com")
    to_email = Email(usermail)
    email_body = "please see attached notification"
    content = Content("text/html", email_body)

    pdf_path = 'out.pdf'

    with open(pdf_path,'rb') as f:
        data = f.read()
        f.close()


    encoded = base64.b64encode(data).decode()

    attachment = Attachment()
    attachment.content = encoded 
    attachment.type = "application/pdf"
    attachment.filename = "test.pdf"
    attachment.disposition = "attachment"
    attachment.content_id = "some content id"

    mail = Mail(from_email, subject, to_email, content)
    mail.add_attachment(attachment)

    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)



def write_html(name, time, amt, address, uid, destination):

    amount = '$'+amt+'.00'

        
    html_str = """<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta name="viewport" content="width=device-width" />

	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>To: Dr. Kim</title>

	<link rel="stylesheet" type="text/css" href="stylesheets/email.css" />

</head>

<body bgcolor="#FFFFFF">

	<table class="head-wrap" bgcolor="#ffffff">

		<td class="header container">

			<div class="content">
				<table bgcolor="#ffffff">


					<img src="logo.png" width="40" height="40" align="right" />


					<h3>Pill Dispenser</h3>
			</div>

		</td>
		<td></td>
		</tr>
	</table><!-- /HEADER -->


	<!-- BODY -->
	<table class="body-wrap">
		<tr>
			<td></td>
			<td class="container" bgcolor="#FFFFFF">

				<div class="content">
					<table>
						<tr>
							<td>
								<h3>To: Dr.Kim</h3>
								<p class="lead">Patient's Prescription</p>
								<p>Patient Name: Ben</p>
								<p>Patient ID: 2</p>
								<p>Prescription Details</p>
								<p>Medication Name:Cocaine</p>
								<p>Dosage: 2</p>
								<p>Refillable: Yes 4</p>
								<p>Prescription Status: Missing</p>
								<p class="callout">
								</p><!-- /Callout Panel -->

								<!-- social & contact -->
								<table class="social" width="100%">
									<tr>
										<td>

											<!-- column 1 -->
											<table align="left" class="column">
											</table><!-- /column 1 -->

											<!-- column 2 -->
											<table align="left" class="column">
												<tr>
													<td>

														<h5 class="">Contact Info:</h5>
														<p>Phone: <strong>408.341.0600</strong><br />
															Email: <strong><a href="emailto:help@pilldispenser.com">help@pilldispenser.com</a></strong></p>

													</td>
												</tr>
											</table><!-- /column 2 -->

											<span class="clear"></span>

										</td>
									</tr>
								</table><!-- /social & contact -->

							</td>
						</tr>
					</table>
				</div><!-- /content -->

			</td>
			<td></td>
		</tr>
	</table><!-- /BODY -->

	<!-- FOOTER -->


	</td>
	<td></td>
	</tr>
	</table><!-- /FOOTER -->

</body>

</html>"""


    Html_file= open("notice.html","w")
    Html_file.write(html_str)
    Html_file.close()



def uploadtobucket(filename, bucketname):
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('gc.json')

    # Make an authenticated API request
##    buckets = list(storage_client.list_buckets())
##    print(buckets)

    bucket = storage_client.get_bucket(bucketname)

    destination_blob_name = filename
    source_file_name = filename

    blob = bucket.blob(destination_blob_name)
    
    blob.cache_control = "no-cache"
    blob.upload_from_filename(source_file_name)
    ##blob.make_public()
    blob.cache_control = "no-cache"

    print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))


@app.route("/dispenseyes", methods=['GET', 'POST'])
def yes():

    ##res = request.json

    s = "Dear Caregiver, Your patient Mr Sick has dispensed medication according to prescription ID 17."
    command = " python twiliogenericsmssender.py 14075648208 " + s
    os.system(command)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp

@app.route("/dispenseno", methods=['GET', 'POST'])
def no():

    ##res = request.json

    s = "Dear Caregiver, Your patient Mr Sick has not dispensed medication according to prescription ID 17. Please check on the status of your patient."
    command = " python twiliogenericsmssender.py 14075648208 " + s
    os.system(command)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp


@app.route("/dummy", methods=['GET', 'POST'])
def dummy():

    ##res = request.json

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp

@app.route("/prescribe", methods=['POST'])
def prescribe():

    ##res = request.json

    global currpresid
    currpresid = currpresid +1

    vals = request.json

    ##print (vals["prescriptionID"])
    ##get max prescription id

    print (vals["patientID"])
    print (vals["medicationName"])
    print (vals["dosage"])
    print (vals["refillable"])
    
    collection = db["patients"]

    s = '{ "prescriptionID": "'+str(currpresid)+'", "patientID" : "' + vals["patientID"] +'", "medicationName": "' + vals["medicationName"] +'", "dosage": "' + vals["dosage"] +'", "refillable": "' + vals["refillable"] +'" }'

    print("qrstring is " + s) 
  
    # Generate QR code 
    url = pyqrcode.create(s) 
      
    # Create and save the png file naming "myqr.png" 
    url.png("prescription.png", scale = 8)

    js = "<html> <body>OK Prescription updated</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    uploadtobucket('prescription.png', 'marquettehealthhacks')

    command = "python twiliogenericsmssender.py 15402302625 https://storage.googleapis.com/marquettehealthhacks/prescription.png Hello, you have a new prescription. please use the QR code provided for dispensing your medication. Thank you."
    os.system(command)

    data = json.loads(s)
    prescriptions = db.prescriptions

    prescriptions.insert_one(data)

    return resp

@app.route("/getradslive", methods=['GET','POST'])
def getradslive():

    res = request.json

    ##vals = request.json

    ##print (vals["prescriptionID"])
    ##get max prescription id

    
    db2 = cluster["radose"]

    live = db2.live
    hist = db2.historical

    myquery = { "userid": "Prashant Bhandari" }

    mydoc = live.find(myquery)

    for x in mydoc:
      print(x)
      print(x["data"])
      data_in = dumps(x["data"])

    

    ##data_in = '{ "data" : ["35", "41", "36", "26", "45", "48", "52", "53", "41"] }'
    data = json.loads(data_in)
    dat =json.dumps(data)

    print(dat)

    js = "<html> <body>OK Prescription updated</body></html>"

    resp = Response(dat, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp


@app.route("/getradslive2", methods=['GET','POST'])
def getradslive2():

    res = request.json

    ##vals = request.json

    ##print (vals["prescriptionID"])
    ##get max prescription id

    
    data_in = '{ "data" : ["35", "41", "36", "26", "45", "48", "52", "53", "41"] }'
    data = json.loads(data_in)
    dat =json.dumps(data)

    print(dat)

    js = "<html> <body>OK Prescription updated</body></html>"

    resp = Response(dat, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp

@app.route("/getrads", methods=['GET','POST'])
def getrads():

    res = request.json

    ##vals = request.json

    ##print (vals["prescriptionID"])
    ##get max prescription id

    
    data_in = '{ "data" : ["21", "0", "0", "185", "0", "0", "26", "34", "0"] }'
    data = json.loads(data_in)
    dat =json.dumps(data)

    print(dat)

    js = "<html> <body>OK Prescription updated</body></html>"

    resp = Response(dat, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp

    



@app.route("/generate2", methods=['POST'])
def generate2():

    vals = request.json



##    name = request.args.get('name')
##    time = request.args.get('time')
##    amount = request.args.get('amount')
##    address = request.args.get('address')
##    uid = request.args.get('uid')
##    destination = request.args.get('destination')

    write_html(vals["name"], vals["time"], vals["amount"], vals["address"], vals["id"], vals["destination"])
    print (vals["email"])


    
    js = "<html> <body>OK</body></html>"

    resp = Response(js, status=200, mimetype='text/html')
    ##resp.headers['Link'] = 'http://google.com'

    return resp



if __name__ == "__main__":
    app.run(debug=True,  port = 8001)
    ##app.run(debug=True, host = '10.192.229.195', port = 8002)
    ##app.run(debug=True, host = '192.168.43.215', port = 8002)





##with open('example.json', 'r') as f:
##    vals = json.load(f)
##
##write_html(vals["name"], vals["time"], vals["amount"], vals["address"], vals["id"], vals["destination"])
##
##print (vals["email"])
