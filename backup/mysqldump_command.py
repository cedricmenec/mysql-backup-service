import subprocess
import os

from datetime import datetime

from commons.commands import ExecutableCommand
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
    
    
    def execute(self, user = None, password = None, database = None, output_path = None):
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
    
    
    
class RestoreDatabaseCommand(ExecutableCommand):
    """
    """
    
    # TODO: Externalize these paths
    binary_directory_path = '/usr/bin'
    binary_filename = 'mysql'
    dump_directory_path = "/tmp/"
    
    def __init__(self):
        self.binary_path = os.path.join(self.binary_directory_path, self.binary_filename)    
    
    
    def execute(self, **args):
        
        # Build the command for subprocess call
        cmd = self.build_command_aguments(args)
        
        command_result = MysqlDumpCommandResult()
        
        if args.get("dump") is None:
            command_result.has_error = True
            command_result.error_cause = "Required argument 'dump' is missing"
            return command_result
        
        dump_path = os.path.join(self.dump_directory_path, args.get("dump"))
        if not os.path.isfile(dump_path):
            command_result.error_cause = "Dump file does not exist : '{}'".format(dump_path)
            command_result.has_error = True
            return command_result
        
        # Open the dump file and pass it to input
        # It is like piping the input  : mysql [options] database < file.dmp
        f = open(dump_path,  'rb')
        try:
            command_result.result_code = subprocess.call(cmd, stdin=f)
        finally:
            f.close()
        
        return command_result
    
        
        
        
    def build_command_aguments(self, args):
        args_list = []
        self.validate_arguments(args)
        args_list.append(self.binary_path)
        args_list.append("--user={}".format(args.get("user")))
        args_list.append("--password={}".format(args.get("password")))
        args_list.append("--protocol=tcp")
        args_list.append(args.get("database"))
        return args_list
    
    
    def validate_arguments(self, args):
        """
        """
        
        if args.get("user") is None:
            raise ValueError("Missing required argument: 'user'")
        if args.get("password") is None:
            raise ValueError("Missing required argument: 'password'")
        if args.get("dump") is None:
            raise ValueError("Missing required argument: 'dump_file'")
        if args.get("database") is None:
            raise ValueError("Missing required argument: 'database'")