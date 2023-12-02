# Telegram Message Sender

This is a Python module designed to send messages and images to bots or groups on Telegram using the Telegram API, AWS Lambda, AWS DynamoDB, and AWS S3. It is particularly useful for notifying members of a recipient list.

## CloudFormation Template for Telegram Message Sender

All the resources needed to deploy the application on AWS can be created via CloudFormation and are described in the `cloudformation.yaml` file.

### `TelegramRestApi`
- API Gateway for the application. This API is one of the simplest ways to create HTTP/HTTPS access for an application.

### `TelegramRestApiDeployment`
- Deployment configuration for the API Gateway.

### `TelegramApiGatewayResource`
- Resource configuration for the API Gateway.

### `TelegramApiGatewayMethod`
- Method designated for handling HTTP requests (GET).

### `TelegramFunctionApiGatewayPermission`
- Permission to invoke the Lambda function.

### `TelegramLambdaFunctionRole`
- IAM role to apply the necessary permissions to the Lambda function.

### `TelegramLambdaFunction`
- Lambda function with the code to be executed. Note that we will copy the code from an S3 bucket. There is a time limit (timeout) for executing the function, and environment variables are available configured textually.

### `TelegramDynamoTable`
- DynamoDB table to save the message history.

## CloudFormation Outputs

The outputs show some information and configurations of what was created.

### `RestAPI`
- ID of the REST API created in the API Gateway.

### `LambdaFunctionRole`
- Name of the IAM role created for the Lambda function.

### `LambdaFunction`
- Name of the Lambda function.

### `AccessURL`
- Created access endpoint, i.e., the URL used to trigger your Lambda function.

### `DynamoTelegramTable`
- Message history table for DynamoDB.

## Python Code

* **Asynchronous Sending**: Messages are sent asynchronously to different destinations using threads, improving sending efficiency and reducing code execution time.
* **DynamoDB Storage**: Sent messages are stored in a DynamoDB database, facilitating tracking and later analysis.
* **S3 Storage**: A text file version of the message is uploaded to an S3 bucket, providing a backup copy and facilitating file management.

### Configuration

Before using this module, it is necessary to configure the following variables and files:

* **AWS Credentials**: Make sure to have AWS credentials configured in the environment where the script will run or the correct permissions in your Lambda function.
* **IMAGE_LIST**: Configure this environment variable with the list of images you intend to use.
* **DESTINATION_LIST**: Configure this variable with the access information for the bots or groups receiving the messages.
* **message_and_config.py**: This file contains project-specific information, such as Telegram bot tokens, chat IDs, and message-related settings. An example is provided as a reference (message_and_config_example.py).

### Usage

The module is designed to be used as an AWS Lambda function. Simply configure a Lambda function in the AWS Management Console and attach this script as the function handler.

When calling the function, provide query parameters such as title and message to send messages to the configured destinations.

Example Lambda function call:

```python
event = {
    "queryStringParameters": {
        "title": "Title: AWS Workshop In Practice: Online and Free Event.",
        "message": "Here you learn to build an application using AWS services to send simultaneous messages to several of your contacts."
    }
}
print(lambda_handler(event, None))
```

Refer to more details in the `commands_to_test.sh` file for local or remote execution.

### Notes
* Ensure that the DynamoDB table and S3 bucket specified in the script are correctly configured and accessible.
* Telegram bot tokens and other sensitive details should not be exposed in the code. Use environment variables or secure methods of storing secrets.
* This module is configured to handle AWS Lambda events but can be adapted for other environments as needed.
* Refer to the documentation of the Telegram Bot API and AWS for detailed information on configuring and using the mentioned services.
