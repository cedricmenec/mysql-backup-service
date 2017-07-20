
class MysqlDumpCommandResult(object):
    """ Represents a mysqldump command execution result """
    
    status = -1    
    result_code = -1
    
    has_error = False
    error_cause = None
    
    
    # MysqlDumpCommand object
    command = None
    
    def __init__(self):
        status = -1
        result_code = -1
        has_error = False