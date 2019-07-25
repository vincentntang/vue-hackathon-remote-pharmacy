import sys
import time
import json
from twilio.rest import Client

with open('credentials.json', 'r') as f:
    creds = json.load(f)


account_sid = creds["twilio"]["account_sid"]
auth_token  = creds["twilio"]["auth_token"]
sender = creds["twilio"]["sender"]

##print (account_sid)
##print (auth_token)

client = Client(account_sid, auth_token) 

##sender = sys.argv[1]
receiver = sys.argv[1]
mediaurl = sys.argv[2]
text = " ".join(sys.argv[3:len(sys.argv)])



message = client.messages.create( 
                              from_=sender,  
                              body=text, 
                              media_url=mediaurl,     
                              to=receiver 
                          )



print(message.sid)
