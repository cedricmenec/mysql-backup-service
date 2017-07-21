from datetime import datetime
import subprocess
import os

from backup.mysqldump_command import MysqlDumpCommand, RestoreDatabaseCommand



def create_backup(**args):
    """ 
        Creates a database backup using mysqldump command.
        i.e mysqldump --user=my_user --password=my_password --databases database_name --single-transaction --result-file=/data/backup/database_name_20170706_0009.dmp     
        If one of the required parameters cannot be propertly evaluated an exception is thrown.
        
        Returns the full path to the backup file or None if error.
    """
    
    # TODO: Externalize this path
    output_path = "/tmp/"

    cmd = MysqlDumpCommand()
    operation_result = cmd.execute(args.get('user'), args.get('password'), args.get('database'), output_path)
            
    return operation_result


def restore_backup(**kwargs):
    """
    Restore a database from a given dump filename.
    
    Arguments:
    filename (String) -- Short filename (without path) of the dump
    database (String) -- Database name to restore
    
    """
    
    cmd = RestoreDatabaseCommand()
    cmd_result = cmd.execute(**kwargs)
    return cmd_result
