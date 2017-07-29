from twilio.rest import Client
import default_config as config
import time
from datetime import date

# Your Account SID from twilio.com/console
account_sid = config.account_sid
# Your Auth Token from twilio.com/console
auth_token = config.auth_token

client = Client(account_sid, auth_token)

# Let us for the moment assume that some inputs have been taken.
# They are a service_id, service_name, wait_time
# These will be hard coded for the moment
# Have to scrape the NHS Choices again to generate service_name from service_id
# TODO Change these to automatically generated from NHS call handler

# service_id = "RW3RE"
# service_name = "Manchester Eye Hospital"
# wait_time = 4
# wait_time_seconds = wait_time * 3600
date = date.today()


def send_messages(name, phone_number, service_id, service_name, wait_time):
    message_1 = client.messages.create(
        to=phone_number,
        from_=config.twilio_number,
        body="REMINDER: Thank you %s for calling NHS 111 today (%s)\n"
             "You were advised to attend %s in %s hours. "
             "Click here for directions: http://0.0.0.0:5000/map/%s" % (name, date, service_name, wait_time,
                                                                        service_id)
        )
    print(message_1.sid)

    # For demo purposes this is set to one minute.
    # In reality will be set to variable wait_time_seconds
    time.sleep(15)

    message_2 = client.messages.create(
        to=phone_number,
        from_=config.twilio_number,
        body="FEEDBACK REQUEST:\n"
             "Would you like to provide anonymous feedback on your recent visit to %s on %s. "
             "Which will improve service in the future."
             "Please click: http://0.0.0.0:5000/show_feedback/%s" % (service_name, date, service_id)
        )
    print(message_2.sid)