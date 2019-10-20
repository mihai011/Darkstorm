from __future__ import absolute_import, print_function, unicode_literals
import boto3


def clean_old_lambda_versions(marker = ''):
    client = boto3.client('lambda')
    if marker == '':
    	functions = client.list_functions()
    else:
	    functions = client.list_functions(Marker=marker)			
    for function in functions['Functions']:
	    while True:
          	versions = client.list_versions_by_function(FunctionName=function['FunctionArn'])['Versions']
          	if len(versions) == 1:
                  version = versions[0]
                  name = version['FunctionName']
                  client.delete_function(FunctionName=name)
                  print('{}: done'.format(function['FunctionName']))
                  break
          	for version in versions:
              		if version['Version'] != function['Version']:
                  		arn = version['FunctionArn']
                  		print('delete_function(FunctionName={})'.format(arn))
                  		client.delete_function(FunctionName=arn)  # uncomment me once you've checked
    if 'NextMarker' in functions:clean_old_lambda_versions(functions['NextMarker'])  
        

if __name__ == '__main__':
    clean_old_lambda_versions()