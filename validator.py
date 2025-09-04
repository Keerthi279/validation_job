from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, EXCLUDE

app = Flask(__name__)

DUMMY_AUTH_TOKEN = "ACCESS_TOKEN_FOR_API_AUTHENTICATION"

class ValidationJobSchema(Schema):
    dataset_id = fields.Str(required=True)
    as_of_date = fields.Str(required=True)
    table = fields.Str(required=False, allow_none=True)
    table_group = fields.Str(required=False, allow_none=True)

class HeaderSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    x_api_key = fields.Str(required=True, data_key="X-Api-Key")
    request_id = fields.Str(required=True, data_key="Request-Id")


validation_job_schema = ValidationJobSchema()
header_schema = HeaderSchema()


def validate_request_header(request):
    try:
        print(request.headers)
        headers = header_schema.load(dict(request.headers))
    except ValidationError as err:
        return err.messages, 400

    if headers["x_api_key"] != DUMMY_AUTH_TOKEN:
        return "Invalid API Key", 403

    return headers, 200


def validate_validation_job(request):
    try:
        data = validation_job_schema.load(request.json)  # validates + deserializes
    except ValidationError as err:
        return err.messages, 400
    
    return data, 200
