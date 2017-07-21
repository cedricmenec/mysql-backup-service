import json
import pprint as pprint
from flask import Blueprint, request, jsonify
from app import app
from backup.schemas.mysqldump_command_result_schema import MysqlDumpCommandResultShema 

import backup.services as services

api = Blueprint('api.backup',  __name__)


@api.route('/', methods=['POST'])    
def create_backup():
    """Create a database backup."""
    data = request.get_json()
    cmd_result = services.create_backup(**data)
    
    schema = MysqlDumpCommandResultShema()
    result = schema.dump(cmd_result)
    return jsonify(result.data)