from marshmallow import Schema, fields, ValidationError, EXCLUDE

class HeaderSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    x_api_key = fields.Str(required=True, data_key="X-Api-Key")
    request_id = fields.Str(required=True, data_key="Request-Id")
