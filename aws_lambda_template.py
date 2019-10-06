import boto3
import logging
import json

def handler(event, context):
    
    #get connections
    with open("connection_file.json") as f:
        connections = json.loads(f.read())

    connections = connections["connections"]

    client = boto3.client('lambda')

    for function in connections:
        client.invoke(FunctionName=function,\
        InvocationType="Event")

