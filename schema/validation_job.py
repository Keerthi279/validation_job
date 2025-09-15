from marshmallow import Schema, fields, ValidationError, EXCLUDE


class ValidationJobSchema(Schema):
    user_id = fields.Str(required=True)
    dataset_id = fields.Str(required=True)
    as_of_date = fields.Str(required=True)
    table = fields.Str(required=False, allow_none=True)
    table_group = fields.Str(required=False, allow_none=True)

class ValidationJobSuccessSchema(Schema):
    status = fields.Str(required=True)
    message = fields.Str(required=True)
    user_id = fields.Str(required=True)
    request_id_received = fields.Str(required=True)
    data_received = fields.Dict(required=True)

class ValidationJobRecordsSchema(Schema):
    status = fields.Str(required=True)
    message = fields.Str(required=True)
    data = fields.List(required=True)
