import json

import boto3
import botocore

def read_configuration(path):

    with open(path) as f:
        data = json.loads(f.read())

    #get functions names

    connections = data["configuration"]

    functions_send = connections.keys()

    functions_recv = connections.values()
    all_functions_recv = []
    for fset in functions_recv:
        all_functions_recv += fset
    
    functions = set(functions_send + all_functions_recv)

    return connections, functions

def read_lambda_conf(path):

    with open(path) as f:
        data = json.loads()

    return data["lambda_conf"]


def main(configuration_path, lambda_conf_path):

    connections, functions = read_configuration("conf.json")
    lambda_conf = read_lambda_conf("lambda_conf.json")

    #create lambda functions 

    for function_name in functions:
        


    