import boto3
import json
def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    foodAvailable = ['Chinese', 'Intalian', 'Japanese','American','Mexician']
    
    
    if intent_name == "GreetingIntent":
        return {
            "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Hello, What can I do for you"
                }
            }
        }
    elif intent_name == "ThankIntent":
        return {"dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "You are more than welcome"
                }
            }
        }
        
    elif intent_name == "Suggestions":
        slot = intent_request['currentIntent']['slots']
        foodtype = slot["FoodType"]
        time = slot['Time']
        location = slot['Location']
        people = slot['People']
        phone = slot['Phone']
        date = slot['Date']
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName='queue1-CC')
        message = json.dumps(slot)
        response = queue.send_message(MessageBody= message)
        print(response.get('MessageId'))
        return {"dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "We would make send message to you about {} at {}".format(foodtype,time)
                }
            }
        }
    else :
        return  {"dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "I cannot get your information done"
                }
            }
        }
        
    
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    
    
    response = {"dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Message to convey to the user."
                }
            }
        }

    return dispatch(event)
