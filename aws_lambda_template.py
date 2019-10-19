import boto3
import logging
import json

logging.basicConfig(level=0, format='%(message)s')
logger = logging.getLogger()

def make_log(msg_type, message):

    if msg_type == "info":
        logger.setLevel(logging.INFO)
        logger.info(message)
    if msg_type == "debug":
        logger.setLevel(logging.DEBUG)
        logger.debug(message)
    if msg_type == "warning":
        logger.setLevel(logging.WARNING)
        logger.warning(message)
    if msg_type == "error":
        logger.setLevel(logging.ERROR)
        logger.error(message)
    if msg_type == "critical":
        logger.setLevel(logging.CRITICAL)
        logger.critical(message)


def handler(event, context):
    
    #get connections
    with open("connection_file.json") as f:
        connections = json.loads(f.read())

    connections = connections["connections"]

    client = boto3.client('lambda')

    for function in connections:
        client.invoke(FunctionName=function,\
        InvocationType="Event")
        make_log("error", "{} {} ".format(function, "called"))

