from marshmallow import Schema, fields, pprint

class MysqlDumpCommandResultShema(Schema):
    result_code = fields.Integer()
    has_error = fields.Boolean()
    error_cause = fields.Str()
    command = fields.Str()
    
    