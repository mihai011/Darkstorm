import json
import zipfile
import os

import boto3
import botocore
import logging


from botocore.exceptions import ClientError

def read_configuration(path):

    with open(path) as f:
        data = json.loads(f.read())

    #get functions names

    connections = data["configuration"]

    functions_send = list(connections.keys())

    functions_recv = connections.values()
    all_functions_recv = []
    for fset in functions_recv:
        all_functions_recv += fset
    
    functions = set(functions_send + all_functions_recv)

    return connections, functions

def read_lambda_conf(path):

    with open(path) as f:
        data = json.loads(f.read())

    return data["lambda_conf"]

def precreate_lambda(template, function_name, connections):

    zip = zipfile.ZipFile(function_name + ".zip",'a')
    zip.write(template,"main.py")
    connection_file = "connection_{}.json".format(function_name)
    with open(connection_file, 'w+') as f:
        f.write(str(connections[function_name]))
    zip.write(connection_file, os.path.basename(connection_file))
    zip.close()

def delete_lambda(client, function_name):
    try:
        client.delete_function(FunctionName=function_name)
    except ClientError as e:
        pass

def create_lambda(client, function_name, conf):

    conf["FunctionName"] = function_name
    with open("{}.zip".format(function_name), mode='rb') as f: 
        archive = f.read()
    conf["Code"] = {"ZipFile":archive}

    try:
        client.create_function(**conf)
    except ClientError as e:
        logging.error(e)

def main(template_path, configuration_path, lambda_conf_path):

    connections, functions = read_configuration("conf.json")
    lambda_conf = read_lambda_conf("lambda_conf.json")

   
    #deletes previous versions and create lambda functions 
    client = boto3.client('lambda')
    for function_name in functions:
        delete_lambda(client, function_name)
        precreate_lambda(template_path, function_name, connections)
        create_lambda(client, function_name, lambda_conf)
    
    logging.info("Functions created!")

    
if __name__ == "__main__":

    template_path = "aws_lambda_template.py"
    configuration_path = "conf.json"
    lambda_conf_path = "lambda_conf_path.json"

    main(template_path, configuration_path, lambda_conf_path)