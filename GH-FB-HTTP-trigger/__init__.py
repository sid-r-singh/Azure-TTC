import logging
import json
import pyrebase
import requests
import pytz
import os
from datetime import datetime
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Obtain info from JSON payload
    body = req.get_json()
    print(body)
    print(type(body))
    sim_type=body['sim_name']
    if sim_type=="MC":
        print("Detected MC sim")
        if type(body['trials']=='int' and type(body['user_name'])=='string'):
            print('All is well. Sairam.')
            #Forward request to Github REST API
            
            #Upon success, add IST time & send to FB
            
            #FB setup
            config = {
            "apiKey": os.environ["fb_apiKey"],
            "authDomain": os.environ["fb_authDomain"],
            "databaseURL": os.environ["fb_databaseURL"],
            "storageBucket": os.environ["fb_storageBucket"]
            }
            firebase = pyrebase.initialize_app(config)
            auth = firebase.auth()

            # Log the user in
            fb_user = os.environ["fb_user_email"]
            fb_pswd = os.environ["fb_pswd"]
            user = auth.sign_in_with_email_and_password(fb_user, fb_pswd)
            url = 'https://mt-iot-brn.firebaseio.com/tg-gh-fb-logs.json?auth='+ user['idToken']
            headers = {
            'Content-Type': 'application/json'
            }
            
            #Add time info to payload
            time_zone = pytz.timezone('Asia/Kolkata')
            current_ts = datetime.now(time_zone) 
            time_string = current_ts.strftime('%d-%m-%Y %H:%M:%S')
            body['IST_time'] = time_string
            
            #Send data to FB
            data = body
            response = requests.request(
            'POST',
            url,
            json=data,
            )

            #Print server response
            print(response)
            print(response.json())
            
        else:
            print("All is not good")
    else:
        logging.info('Not MC')
        
    return func.HttpResponse('Success')