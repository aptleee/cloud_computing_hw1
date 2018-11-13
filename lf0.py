import json
import boto3
def lambda_handler(event, context):
    client = boto3.client('lex-runtime')
    response1 = client.post_text(
        botName='RestaurantBooking',
        botAlias='$LATEST',
        userId='Ximing',
        inputText= event['input']
    )

    # pass
    return {
        "statusCode": 200,
        "body": response1["message"]
    }
