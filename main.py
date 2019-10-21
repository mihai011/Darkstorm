import json
import zipfile
import os
import sys
import uuid

import boto3
import botocore

from botocore.exceptions import ClientError

from utils import detect_cycles, make_log

def show_banner(file):

    with open(file) as f:
        print(f.read())

def write_configuration(layers, path):

    all_functions = []
    structure = {}
    for i in range(len(layers)):
        structure[i] = []
        for j in range(layers[i]):
            id = str(uuid.uuid4())
            structure[i].append(id)
            all_functions.append(id)

    conf = {}
    conf["trigger_functions"] = structure[0]

    conf["configuration"] = {f:[] for f in all_functions}

    for key in structure.keys():
        for f in structure[key]:
            if key+1 not in structure:
                conf["configuration"][f] = []
            else:
                conf["configuration"][f] = structure[key+1]

    with open(path, 'w') as f:
        f.write(json.dumps(conf, indent=4))
        

def read_configuration(path):

    with open(path) as f:
        data = json.loads(f.read())

    #get functions names
    connections = data["configuration"]
    trigger_functions = data["trigger_functions"]

    functions_send = list(connections.keys())

    functions_recv = connections.values()
    all_functions_recv = []
    for fset in functions_recv:
        all_functions_recv += fset
    
    functions = set(functions_send + all_functions_recv)
    
    #detect cycles
    """
    visited_journal = {f:False for f in functions}
    cycles = []
    for trigger_function in trigger_functions:
        cycles.append(detect_cycles(trigger_function, connections, visited_journal))

    if True in cycles:
        make_log("critical", "Configuration contains cycles")
        sys.exit(0)
    else:
        make_log("info","Configurations does not contain cycles")
    """
    return connections, functions, trigger_functions

def read_lambda_conf(path):

    with open(path) as f:
        data = json.loads(f.read())

    return data["lambda_conf"]

def read_layers(path):

    with open(path) as f:
        data = json.loads(f.read())

    layers = data["layers"]

    dimension_chain = []
    for layer in layers:
        if layer[0] == "fully_connected":
            dimension_chain += layer[1:3]

    #check dimensions
    common_dimensions = dimension_chain[1:-1]
    interior_distance = []
    for i in range(0, len(common_dimensions), 2):
        if common_dimensions[i] != common_dimensions[i+1]:
            make_log("critical", "Error in layer dimensions")
            sys.exit(0)
        else:
            interior_distance.append(common_dimensions[i])

    interior_distance.insert(0, dimension_chain[0])
    interior_distance.append(dimension_chain[-1])

    return interior_distance

def precreate_lambda(template, function_name, connections):

    archive_name = "{}.zip".format(function_name)
    connection_file = "connection_file.json"

    if os.path.exists(archive_name):
        os.remove(archive_name)

    if os.path.exists(connection_file):
        os.remove(connection_file)

    zip = zipfile.ZipFile(archive_name,'a')
    zip.write(template,"main.py")
    
    with open(connection_file, 'w+') as f:
        cell = {}
        cell["connections"] = connections[function_name]
        f.write(json.dumps(cell))
        
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
        res = client.create_function(**conf)
        make_log("info", "Function '{}' called with status:{}".format(function_name, res["ResponseMetadata"]["HTTPStatusCode"]))
        os.remove("{}.zip".format(function_name))
    except ClientError as e:
        make_log("error", e)


def call_function(client, function_name, event):
    
    res = client.invoke(FunctionName=function_name,\
         InvocationType = "Event")
    make_log("info", "Function '{}' called with status:{}".format("invoke",res["StatusCode"]))

def main(template_path, configuration_path, lambda_conf_path):

    connections, functions, trigger_functions = read_configuration("conf.json")
    lambda_conf = read_lambda_conf("lambda_conf.json")
    make_log("info","Configurations read!")

    #deletes previous versions and create lambda functions 
    client = boto3.client('lambda')
    for function_name in functions:
        delete_lambda(client, function_name)
        precreate_lambda(template_path, function_name, connections)
        create_lambda(client, function_name, lambda_conf)
    
    make_log("info","Functions created!")

    #invoke lambda
    event = {}
    for trigger_function in trigger_functions:
        call_function(client, trigger_function, event)

    make_log("info", "Trigger functions called!")
    
if __name__ == "__main__":

    show_banner("banner.txt")

    template_path = "aws_lambda_template.py"
    configuration_path = "conf.json"
    lambda_conf_path = "lambda_conf_path.json"

    layers = read_layers("layers_conf.json")

    #create lower level configurations

    write_configuration(layers, configuration_path)
    

    main(template_path, configuration_path, lambda_conf_path)