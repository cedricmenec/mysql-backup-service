import subprocess
import os

from datetime import datetime

from backup.mysqldump_command_result import MysqlDumpCommandResult


class MysqlDumpCommand(object):
    """ Represents a mysqldump command """
    
    binary_root_path = '/usr/bin'
    binary_name = 'mysqldump'
    binary_path = os.path.join(binary_root_path, binary_name)
    
    
    def __init__(self):
        """
        Constructor
        """
        pass
    
    
    def execute(self, user = None, password = None, database = None, output_path = None, **kwargs):
        """        
        Raises ValueError exception if required argument is missing.
        """            
        command_args = {}
        command_args["user"] = user
        command_args["password"] = password
        command_args["database"] = database
        
        result = MysqlDumpCommandResult()
        
        try:
            self.validate_arguments(command_args)
            
            if output_path is None:
                raise ValueError('Output path is required')
        except ValueError as e:
            result.has_error = True
            result.error_cause = "Validation error : {}".format(e.strerror)
            
         # Compute dump output filename
        now_timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = "{}-{}.dmp".format(database, now_timestamp) 
        file_path = os.path.join(output_path, filename)
        command_args["output_file"] = file_path        

        try:
            cmd_args = self.build_command_args(command_args)
        except ValueError as e:
            result.has_error = True
            result.error_cause = e.strerror
            return result
    
    
        # Execute command :
        result.result_code  = subprocess.call(cmd_args)
        result.command = ' '.join(cmd_args)
        
        if result.result_code != 0:
            result.has_error = True
            result.error_cause = self.get_mysqldump_error_cause(result.result_code, command_args)
            
            # Sometime, when the command failed, an empty dump file is created.
            # If so, we need to delete this unused file.
            if os.path.isfile(file_path) :
                os.remove(file_path)            
            
        return result
    
    
    
    def get_mysqldump_error_cause(self, error_code, context):
        """
        Return a string representing the error that mysqldump has return as an error code.
        
        Arguments:
        error_code (int) -- Error code returned by mysqldump command.
        context (dict) -- A Dict object representing the arguments passed to mysqldump command.
        
        Example:
            > get_mysqldump_error_cause(2, {"user": "john", "database": "bad_db"})
            > "Unknown database [bad_db]"
        """
        
        if error_code == 2 :
            return "Unknown database [{}]".format(context.get("database"))
        else:
            return "unknown error (see mysqldump error_code details)"
            
   

    def validate_arguments(self, args):
        
        user = args.get("user")
        if user is None:
            raise ValueError("user argument is mandatory")
        
        password = args.get("password")
        if password is None:
            raise ValueError("password argument is mandatory")
        
        database = args.get("database")
        if database is None:
            raise ValueError("database argument is mandatory")
            
        
    
    def build_command_args(self, args):
        """
        Builds the mysqldump's command line to execute (in array form) from a dictionnary.
        In case of missing mandatory argument, an ValueError exception is raised.
        
        If success, returns the command's arguments array ready to be passed to subprocess call or Popen functions.
        
        """
        cmd_args = []
        cmd_args.append(self.binary_path)   # this is mysqldump executable path
        
        user = args.get("user")
        if user is None:
            raise ValueError("user argument is mandatory")
        else:
            cmd_args.append("--user={}".format(user))
            
        password = args.get("password")
        if password is None:
            raise ValueError("password argument is mandatory")
        else:
            cmd_args.append("--password={}".format(password))
         
        dump_file_path = args.get("output_file")
        if dump_file_path is None:
            raise ValueError("output_file argument is mandatory")
        else:
            cmd_args.append("--result-file={}".format(dump_file_path))
        
        cmd_args.append("--single-transaction")
        cmd_args.append("--protocol=tcp")
        
        database = args.get("database")
        if database is None:
            raise ValueError("database argument is mandatory")
        else:
            cmd_args.append(database)
                    
        return cmd_args
    
    