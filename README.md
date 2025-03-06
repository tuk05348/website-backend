# Cloud Resume Challenge Backend
![Infrastructure Diagram](/Cloud_Resume_Challenge_Backend.png)

This diagram displays my implementation of the specifications of the Cloud Resume Challenge.

## Background

The [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/) is a challenge where one builds their own personal, static website to host their resume online with a visitor counter, using a Cloud provider like AWS, GCP, or Azure. It involves the entire stack, creating a database to store the visitor count, back-end code to increment the count, an API to deliver the count at a request, and a front-end to make that request.

I have undertaken this challenge and this README documents my attempt at the back-end portion of the challenge. I used AWS SAM to deploy my resources as Infrastructure as Code (IaC): a Lambda Function to increment the visitor count, a DynamoDB table to store the count, and an API Gateway REST API to deliver said count.

## AWS SAM

[AWS SAM](https://aws.amazon.com/serverless/sam/), otherwise known as the AWS Serverless Application Model, is a tool that allows you to define your AWS resources in a template, letting you express your infrastructure as code (IaC). Using AWS SAM, I was able to write a template that defined my Lambda Function, DynamoDB table, and API Gateway Rest API.

An AWS Serverless Function is used to define the Lambda Function (runtime, code URI, permissions) and also defines the REST API as an event that triggers the Lambda function.

## Lambda Function

Calls update_item to update the visitor count by incrementing it by one. An expression is used to create one if the visitor count item does not yet exist yet.

## DynamoDB Table

Holds the visitor count item.

## API Gateway

REST API with a route using a GET request to /visitorcount, the path for the visitor count resource that we get from the Lambda function.

## Testing and Github Actions Workflow

A unit test written in Python checks if the Lambda function increments the count by one. Integration tests written in Python using the requests library test the API Gateway Rest API to make sure requests are successful and that subsequent requests update the count.

Github Actions is used to build the Lambda function, REST API, and DynamoDB table from the AWS SAM template, by using the AWS SAM CLI to build the resources from the template and deploy them in a CloudFormation stack.

After building and before deployment, the unit test is run, and then a staging environment stack is deployed to run the integration tests on a REST API that replicates the production environment.

After the tests pass, the production environment is deployed, creating/updating the CloudFormation stack.
