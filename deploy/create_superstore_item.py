import boto3
import os
import logging
# Make sure all of the important regions have the tables created
regions = os.environ['REGIONS'].split(',')

def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    customer_id = event['customer_id']
    item_id = event['key']
    item_value = event['value']
    for region in regions:
        # Creating new record in DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name=region)    
        table = dynamodb.Table(customer_id)
        logger.info('Writing item to region: {}'.format(region))
        table.put_item(
            Item={
                'id': item_id,
                'value': item_value
            }
        )