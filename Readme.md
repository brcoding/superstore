# SuperStore

SuperStore is a simple application that runs entirely on AWS offering a multi-region highly available API that offers a simple name value store.  This project uses The AWS API Gateway, DynamoDB, S3, and Cloudfront.

# Limitations

* The application swagger documentation is poor due to lack of time.
* The API itself is very rushed and there are some issues:
  - /items/ should have an /items/ GET which returns a full list and /items/{KEY} as a path variable. This a quick resource was added for /items/list to get a full list of items and query strings were used instead baffling the author.
  - The /account/ API resource does not provide any authorization and allows anyone to create a table in DynamoDB. 
  - The DynamoDB implementation has a limit of 256 accounts because each account is tied to a new table. In a more realistic implementation the organization accounts under consolidated billing would be used instead for each customer giving better billing and a specific account for each dynamoDB. My account was not allowed create sub accounts so a table per customer was used instead. This is not ideal.
  - The /items/ resource has no authorization, It should accept either an API key or specific IAM permissions.
* The distribution is done with serverless but the serverless.yml needs a bit more work and testing, the major
  sections are there to show proof of concept but it only mostly works.
* The serverless distribution does not handle setup of the S3 assets and uploading. A helpful script would be nice to upload the swagger document and swagger UI web pages.

# Installation

High Availability for the API Gateway is achieved through the use of Cloudfront using multiple origins. Since the API Gateway cannot be put behind Route53 this is the only way to load balance the API Gateway. Because of this each origin in the serverless.yml must be added for each region. 

Follow this handy guide to install serverless: http://docs.aws.amazon.com/cli/latest/userguide/installing.html

* Log in to AWS
* Import superstore-prod-swagger-apigateway.json in to API gateway for each region
* Update the serverless.yml with the region you wish to push to and update the origin section to match the API Gateway origins you setup in the previous step.
* Update the swagger.json location in the s3/index.html file.
* Upload the contents of the S3 folder to your primary region with replication turned on to at least one other region.

# Usage

## Account Creation

Resource: /account
Method: POST

Input Body Sample:
`{
  "customer_id": "TESTCUSTOMERKEY"
}`

Example Curl Call:

`curl -L -H "Content-Type: application/json" -X POST -d "{\"customer_id\":\"TESTCUSTOMER15\"}" http://d2ldv12x4osxdk.cloudfront.net/account`
---
## Create Key Value Item

Resource: /items
Method: POST

Input Body Sample:
`{
  "customer_id": "TESTCUSTOMERKEY"
  "key": "some key"
  "value": some string value"
}`

Example Curl Call:

`curl -L -H "Content-Type: application/json" -X POST -d "{\"customer_id\":\"TESTCUSTOMER15\", \"key\": \"some key\", \"value\": \"some string value\"}" http://d2ldv12x4osxdk.cloudfront.net/items`
---
## Get Key Value Item

Resource: /items
Method: GET

Query String Parameters:

customer_id: string
key: string

Example Curl Call:

`curl -L -H "Content-Type: application/json" -X GET "http://d2ldv12x4osxdk.cloudfront.net/items?customer_id=TESTCUSTOMER15&key=some%20key"`

Expected Output:

`{"Item": {"id": "some key", "value": "some string value"}, "ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "GA64A1PS2S512HNI1H42AMEONBVV4KQNSO5AEMVJF66Q9ASUAAJG", "HTTPHeaders": {"x-amzn-requestid": "GA64A1PS2S512HNI1H42AMEONBVV4KQNSO5AEMVJF66Q9ASUAAJG", "content-length": "66", "server": "Server", "connection": "keep-alive", "x-amz-crc32": "2054443726", "date": "Tue, 24 Oct 2017 15:54:29 GMT", "content-type": "application/x-amz-json-1.0"}}}`
---
## Get All Key Value Item

Resource: /items/list
Method: GET

Query String Parameters:

customer_id: string

Example Curl Call:

`curl -L -H "Content-Type: application/json" -X GET "http://d2ldv12x4osxdk.cloudfront.net/items/list?customer_id=TESTCUSTOMER15"`

Expected Output:

`{"Count": 1, "Items": [{"id": "some key", "value": "some string value"}], "ScannedCount": 1, "ResponseMetadata": {"RetryAttempts": 0, "HTTPStatusCode": 200, "RequestId": "J3O9DQRSRK3FRBQ8FTRG4AT1A3VV4KQNSO5AEMVJF66Q9ASUAAJG", "HTTPHeaders": {"x-amzn-requestid": "J3O9DQRSRK3FRBQ8FTRG4AT1A3VV4KQNSO5AEMVJF66Q9ASUAAJG", "content-length": "96", "server": "Server", "connection": "keep-alive", "x-amz-crc32": "2657371979", "date": "Tue, 24 Oct 2017 15:56:18 GMT", "content-type": "application/x-amz-json-1.0"}}}`
---
## Delete Key Value Item

Resource: /items
Method: DELETE

Query String Parameters:

customer_id: string
key: string

Example Curl Call:

`curl -L -H "Content-Type: application/json" -X DELETE "http://d2ldv12x4osxdk.cloudfront.net/items?customer_id=TESTCUSTOMER15&key=some%20key"`

# Demo Site:

https://s3.amazonaws.com/superstorewebsite/index.html

NOTE: that this swagger UI has a few issues so does the swagger.json that need to be improved before it is fully funcitonal.