import logging
import json
import pyrebase
import requests
import names
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
        #Check for spams
        if type(body['trials']=='int' and body['trials'] <= 1000000 and type(body['user_name'])=='string' and str(body['is_bot'])=='False'):
            print('All is well. Sairam.')
        #Forward request to Github REST API
            rnd_name = names.get_full_name()
            sender_chat_id = body['chat_id']
            no_of_trials = body['trials']
            status = 400
            try:
                url = 'https://api.github.com/repos/sid-r-singh/Telegram-Python/actions/workflows/python-publish.yml/dispatches'
                headers = {
                'Authorization': os.environ["auth_info"],
                'Content-Type': 'application/json'
                }
                data = "{\"ref\":\"main\",\"inputs\": { \"no_trials\":\""+str(no_of_trials)+"\",\"user_chat_id\":\""+str(sender_chat_id)+"\",\"user_name_ano\":\""+rnd_name+"\"}}"
                r = requests.request(
                'POST',
                url,
                data=data,
                headers=headers,
                )
                r.raise_for_status()
                status=r.status_code
                print(x)
            except requests.exceptions.HTTPError as err:
                print('HTTP error occured:')
                print(err)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print('Other error occured:')
                print(e)
            if status==204:
                print('Success')
            else:
                print('Faileeeed')

        #Upon success, add IST time & send to FB
            
            #FB setup
            # config = {
            # "apiKey": os.environ["fb_apiKey"],
            # "authDomain": os.environ["fb_authDomain"],
            # "databaseURL": os.environ["fb_databaseURL"],
            # "storageBucket": os.environ["fb_storageBucket"]
            # }
            # firebase = pyrebase.initialize_app(config)
            # auth = firebase.auth()

            # Log the user in
            # fb_user = os.environ["fb_user_email"]
            # fb_pswd = os.environ["fb_pswd"]
            # user = auth.sign_in_with_email_and_password(fb_user, fb_pswd)
            # url = 'https://mt-iot-brn.firebaseio.com/tg-gh-fb-logs.json?auth='+ user['idToken']
            # headers = {
            # 'Content-Type': 'application/json'
            # }
            
            #Add time info to payload
            time_zone = pytz.timezone('Asia/Kolkata')
            current_ts = datetime.now(time_zone) 
            time_string = current_ts.strftime('%d-%m-%Y %H:%M:%S')
            body['IST_time'] = time_string

            
            #Send data to FB
            # data = body
            # response = requests.request(
            # 'POST',
            # url,
            # json=data,
            # )

            #Send data to TG
            url = 'https://api.telegram.org/bot'+os.environ['tg_bot_token']+'/sendMessage'
            json_to_str = json.dumps(body,indent=2, sort_keys=True)
            chat_id = str(os.environ["tg_admin_chat_id"])

            headers = {
            'Content-Type': 'application/json'
            }
            data = "{\"chat_id\": \""+chat_id+"\", \"text\":"+ json_to_str+ "}"
            response = requests.request(
            'POST',
            url,
            data=data,
            headers=headers,
            )


            #Print server response
            print(response)
            logging.info(response)
            #print(response.json())
            
        else:
            print("Bad request / request not well formatted")
    else:
        logging.info('Not MC')
        
    return func.HttpResponse('Success')