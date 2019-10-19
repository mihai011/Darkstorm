import logging

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


def detect_cycles(start, connections, visited_journal):


    first_connections = connections[start]
    visited_journal[start] = True

    for connection in first_connections:
        if visited_journal[connection] == False:
            if detect_cycles(connection, connections, visited_journal) == True:
                return True
        elif visited_journal[connection] == True:
            return True

    
    visited_journal[connection] = False
    return False



