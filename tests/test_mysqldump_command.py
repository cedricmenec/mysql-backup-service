import pytest
from backup.mysqldump_command import MysqlDumpCommand, MysqlDumpCommandResult


def test_build_command_args_missing_all_args():
    cmd = MysqlDumpCommand()
    
    with pytest.raises(TypeError):
        cmd.build_command_args()

        
def test_build_command_args_missing_required_args():
    cmd = MysqlDumpCommand()
    
    # database argument is missing
    args = {
        "user": "user",
        "password": "password",
        "output_file": "/tmp/my_file.dmp"        
    }
    
    with pytest.raises(ValueError):
        cmd.build_command_args(args)


def test_build_command_args():
    cmd = MysqlDumpCommand()

    # database argument is missing
    args = {
        "user": "user",
        "password": "password",
        "output_file": "/tmp/my_file.dmp",     
        "database": "database"
    }
    
    cmd_args = cmd.build_command_args(args)
    assert len(cmd_args) == 7
    assert cmd_args[6] == "database"
    