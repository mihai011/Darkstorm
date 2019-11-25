import uuid
import json

def write_configuration_layers(layers, path):

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


def write_configuration_matrix(matrix, path):

    all_functions = []
    func_enc = {}
    for i in range(len(matrix)):
        func_enc[i] = str(uuid.uuid4())

    conf = {}
    conf["trigger_functions"] = [func_enc[0]]

    conf["configuration"] = {f:[] for f in all_functions}

    for i in range(len(matrix)):
        conf["configuration"][func_enc[i]] = []
        for j in range(len(matrix[i])):
            conf["configuration"][func_enc[i]].append(func_enc[j])


    with open(path, 'w') as f:
        f.write(json.dumps(conf, indent=4))