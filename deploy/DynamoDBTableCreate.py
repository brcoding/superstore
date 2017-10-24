import boto3
import os
import logging

# Make sure all of the important regions have the tables created
regions = os.environ['REGIONS'].split(',')

def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for region in regions:
        logger.info('Creating Tables for region {}'.format(region))
        customer_id = event['customer_id']
        #Creating new record in DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.create_table(
            TableName=customer_id,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
        
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        # TODO: Need to add a trigger for this table for replication put_rule?
        logger.info('Updating customer table for region: {}'.format(region))
        table = dynamodb.Table(os.environ['CUSTOMER_TABLE_NAME'])
        table.put_item(
           Item={
                'customer_id': customer_id,
                'customer_table': customer_id
            }
        )
    logger.info('Account Creation Complete')
    return