import json
import boto3
from requests import get
from datetime import datetime

def lambda_handler(event, context):

    # ------------------receive message from sqs------------- #
    
    sqs = boto3.resource('sqs')
    queue = sqs.Queue('')

    for message in queue.receive_messages(MaxNumberOfMessages=10):
        body = json.loads(message.body)
        body = [x.lower() for x in body.values()]
        nop, food, phoneNumber, location, time, date = body
        date = date.split('-')
        time = time.split(':')
        dtp = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1])) 
        dt = int(dtp.timestamp())
    
  
        # ------call yelp api and get three restaurants--------- #
       
        url = 'https://api.yelp.com/v3/businesses/search?term=food&location='+location+'&categories='+food+'&open_at='+str(dt)+'&sort_by=best_match&limit=5'
        h = {'Authorization': ''}
        response = get(url, headers=h)
        response = json.loads(response.text)
        if len(response["businesses"]) == 0:
            smsMessage = "Cannot find suitable restaurant."
        else:
            name1 = response['businesses'][0]['name']
            loc1 = response['businesses'][0]['location']['address1']
            name2 = response['businesses'][1]['name']
            loc2 = response['businesses'][1]['location']['address1']
            name3 = response['businesses'][2]['name']
            loc3 = response['businesses'][2]['location']['address1']
        
            smsMessage = "Hello! Here are my " + food + " restaurant suggestions for " + \
                nop + " people, for today at " + str(dtp) + \
                ": 1. " + name1 + ", located at " + loc1 + \
                ", 2. " + name2 + ", located at " + loc2 + \
                ", 3. " + name3 + ", located at " + loc3 + "." + \
                " Enjoy your meal!"
                
     
        # ------------- send message ------------- #
       
        sns = boto3.client('sns')
        response2 =  sns.publish(PhoneNumber=phoneNumber, Message=smsMessage)
    
      
        # ------------- put the record in dynamoDB --------------- #
       
        response1 = dyn.put_item(
        TableName='Bigtable',
        Item={
            'record': {
                'S': smsMessage+str(body),
            },
            'timestamp': {
                'S': str(datetime.now().timestamp())
            }
        }
        )
        message.delete()
    
    return 0
        



