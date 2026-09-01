import json
import boto3

# Initialize your data tools at the global level for fast execution reuse!
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume-counter')

# Initialize the email delivery service client
ses_client = boto3.client("ses", region_name="us-east-1")

def lambda_handler(event, context):
    try:
        # Keep your existing, excellent DynamoDB state machine incrementer
        response = table.update_item(
            Key={'id': '0'},
            UpdateExpression='ADD #c :val',
            ExpressionAttributeNames={'#c': 'count'},
            ExpressionAttributeValues={':val': 1},
            ReturnValues='UPDATED_NEW'
        )
        
        # Extract the live dynamic value from your persistent database state
        updated_count = int(response['Attributes']['count'])
        
        # Extract visitor details from the web request event dictionary
        headers = event.get("headers", {})
        request_context = event.get("requestContext", {})
        identity = request_context.get("identity", {})

        source_ip = identity.get("sourceIp", "Hidden IP/Local Test")
        user_agent = headers.get("user-agent", "Unknown Device/Browser")
        visitor_country = headers.get("cloudfront-viewer-country", "Global Location")
        
        # Set your target verified personal Gmail account identifier
        sender_email = "JK6366741@GMAIL.COM"
        receiver_email = "jamalkhan74867@gmail.com" 
        
        # Expanded notification body formatting layout
        email_body = (
            f"Hello Muhammad,\n\n"
            f"🚀 A new recruiter just viewed your portfolio website!\n\n"
            f"🔢 Current Live Count: {updated_count}\n"
            f"🌐 Network IP Address: {source_ip}\n"
            f"📍 Estimated Location: {visitor_country}\n"
            f"🖥️ Device Fingerprint: {user_agent}\n\n"
            f"Keep grinding!"
        )
        
        # Send your notification payload straight to your phone inbox
        try:
            ses_client.send_email(
                Source=sender_email,
                Destination={
                    'ToAddresses': [receiver_email]
                },
                Message={
                    'Subject': {
                        'Data': '🚀 New Portfolio Visitor Alert!'
                    },
                    'Body': {
                        'Text': {
                            'Data': email_body
                        }
                    }
                }
            )
        except Exception as email_err:
            print(f"Email delivery failed structural catch: {str(email_err)}")
        
        # Return your successful CORS response headers payload to your frontend JavaScript
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'count': updated_count})
        }
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'count': 0, 'error': str(e)})
        }
