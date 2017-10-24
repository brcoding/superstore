import boto3
import os
import logging
# Make sure all of the important regions have the tables created
regions = os.environ['REGIONS'].split(',')

def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    customer_id = event['customer_id']

    for region in regions:
        # Attempting to access record in DynamoDB customer table
        dynamodb = boto3.resource('dynamodb', region_name=region)    
        table = dynamodb.Table(customer_id)
        logger.info('Getting item from region: {}'.format(region))
        try:
            return table.scan()
        except Exception as e:
            logger.error('Error accessing region or table')
    raise Exception('Unable to access key or invalid customer')