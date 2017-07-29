from twilio.rest import Client
import default_config as config
import time
from datetime import date
import app as data

# Your Account SID from twilio.com/console
account_sid = config.account_sid
# Your Auth Token from twilio.com/console
auth_token = config.auth_token

client = Client(account_sid, auth_token)

# Let us for the moment assume that two inputs have been taken.
# They are a service_id and a time
# These will be hard coded for the moment
# TODO Change these to automatically generated from NHS call handler

service_id_test = "RW3RE"
service_id = data.service_id
print (service_id)
service_name = "Manchester Eye Hospital"
wait_time = 4
date = date.today()

message_1 = client.messages.create(
    to="+447921227896",
    from_=config.twilio_number,
    body="REMINDER: Thank you MR SMITH\n" \
         "We have arranged an appointment for you at %s in %i hours on %s. " \
         "Click here for directions: http://bit.ly/2v6zqKf" % (service_name, wait_time, date))
print(message_1.sid)

time.sleep(120)

message_2 = client.messages.create(
    to="+447921227896",
    from_=config.twilio_number,
    body="FEEDBACK REQUEST:\n"
         "Would you like to provide anonymous feedback on your recent visit to %s on %s."
         "Please click: http://bit.ly/2t4pkZ7" % (service_name, date)
    )
print (message_2.sid)