import logging
import argparse

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


def check_cycles(start, connections, visited_journal):


    first_connections = connections[start]
    visited_journal[start] = True

    for connection in first_connections:
        if visited_journal[connection] == False:
            if check_cycles(connection, connections, visited_journal) == True:
                return True
        elif visited_journal[connection] == True:
            return True

    
    visited_journal[start] = False
    return False

def create_parser():

    parser = argparse.ArgumentParser(description='Get data required by the program. ')
    
    parser.add_argument('--layers-conf',dest='layers_conf_path', type=str,
                        help='layers configuration for a neural net')

    parser.add_argument('--lambda-conf', dest='lambda_conf_path',type=str,
                    help='lambda fuction configuration')

    parser.add_argument('--lambda-template', dest='lambda_template_path',type=str,
                    help='template that represents code that is executed by the lambda')

    parser.add_argument('--check-cycles', dest='check_cycles',type=bool,
                    help='check for cycles in the structure')

    parser.add_argument('--conf-global', dest='conf_global_path',type=str,
                    help='configuration file for full structure')

    parser.add_argument('--matrix-conf-path', dest='matrix_conf_path',type=str,
                    help='configuration file for graph structure')


    return parser.parse_args()