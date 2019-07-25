import sys
import time
import json
from twilio.rest import Client
import os
from twilio.twiml.voice_response import VoiceResponse, Say
from google.cloud import storage

with open('credentials.json', 'r') as f:
    creds = json.load(f)


account_sid = creds["twilio"]["account_sid"]
auth_token  = creds["twilio"]["auth_token"]
sender = creds["twilio"]["sender"]

##print (account_sid)
##print (auth_token)

storage_client = storage.Client.from_service_account_json('gc.json')

client = Client(account_sid, auth_token) 

##sender = sys.argv[1]
receiver = sys.argv[1]
message = " ".join(sys.argv[2:len(sys.argv)])
##soundurl = sys.argv[len(sys.argv)-1]

print (message)
##print (soundurl)


response = VoiceResponse()
response.say(message, voice='Polly.Kimberly')
##response.play('https://api.twilio.com/cowbell.mp3', loop=1)
##response.play(soundurl, loop=1)

print(response)

out = str(response)

file = open("voiceresponse.xml", "w")
file.write(out)
file.close()

bucket = storage_client.get_bucket('marquettehealthhacks')
destination_blob_name = 'voiceresponse.xml'
source_file_name = 'voiceresponse.xml'

blob = bucket.blob(destination_blob_name)
blob.content_type = 'application/xml'

blob.upload_from_filename(source_file_name)
##blob.make_public()

print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))




call = client.calls.create(
                        url='http://storage.googleapis.com/knighthacks/voiceresponse.xml',
                        ##url='http://fit-x-lab.com/hackathonfiles/voiceresponse.xml.txt',
                        to=receiver,
                        from_=sender,
                        method = "GET"
                    )

print(call.sid)