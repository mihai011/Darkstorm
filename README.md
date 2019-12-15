# Darkstorm

![alt text](https://raw.githubusercontent.com/mihai011/Darkstorm/master/A-anim.164.jpg)

Connected AWS Lambdas for the future.

Small framework that helps with experimenting with AWS lambdas on a more "connected" paradigm.

## Installation

No installation required. Just clone the repo and you are good to go.

## Usage

### Graph-matrix based usage
```
python main.py --matrix-conf-path matrix_conf.json --lambda-conf lambda_conf.json --lambda-template aws_lambda_template.py  --conf-global conf.json
```
### Neural network based usage
```
python main.py --layers-conf-path layers_conf.json --lambda-conf lambda_conf.json --lambda-template aws_lambda_template.py  --conf-global conf.json

```

### Parameters 

```
--layers-conf-path
Path to the layer configuration path
```

Example for a layer configuration path.

```
{
    "layers":
    [
        ["fully_connected",1, 2],
        ["fully_connected",3, 2],
        ["fully_connected",1, 2]
    ]   
}
```

```
--matrix-conf-path
Path to the matrix configuration path
```

Example for a matrix configuration path.

```
{
    "matrix":
    [
        [0,0,1],
        [1,0,1],
        [1,0,0]
    ]
}
```

```
--lambda-conf
Path to the file that serves the configuration for a lambda function.
```

Example for a lambda configuration path. Feel free to change these according to your needs.

```
{
    "lambda_conf":
    {
        "Runtime":"python3.7",
        "Role":"Role",
        "Handler":"main.handler",
        "Timeout":10,
        "MemorySize":128
    }
}
```

```
--lambda-template
Path to the file that contains the code which will be deployed to the lambda function.
The example is already in the repo, aws_lambda_template.py.
```

```
--conf-global 
Path to the file where the full configuration of the deployed system is written. It must have the json file extension.
```

```
--check-cycles True/False
```

```
Check for the presence of a cycle in the full structure deployed.
```

## Install Python Requirements 

Although the code was developed in a conda environment i have attached a requirements file to the repo for ease of use with pip3 package manager.

## Special requirements

You must have AWS credentials configured in your system. Preferably in the .aws directory (default location).

## Caution !!!

Abusive usage with high number of lambdas and without cycle check can lead to massive AWS bills.

To delete the lambdas and their attached logs execute delete_log_groups.log' and 'delete_lambdas.py' scripts.


## Journal Security

Began modifying this tool for penetration testing purposes, involving machine learning techniques.

## License

No license attached.