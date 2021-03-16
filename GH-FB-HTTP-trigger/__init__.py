import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Obtain info from JSON payload
    body = req.get_json()
    print(body)
    print(type(body))
    sim_type=body['sim']
    if sim_type=="MC":
        print("Detected MC sim")
        if len(body)==3 and type(body['trials']=='int' and type(body['user_name'])=='string'):
            print('All is good')
            #Forward request to Github REST API
            
            #Upon success, add IST time & send to FB
            
            
        else:
            print("All is not good")
    else:
        logging.info('Not MC')
        
    return func.HttpResponse('Success')