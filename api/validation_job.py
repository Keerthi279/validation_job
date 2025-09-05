from flask import jsonify, request
from flask_smorest import Blueprint
from flask.views import MethodView
from validator.header import validate_request_headers
from validator.validation_job import validate_validation_job
from service.validation_job import process_validation_job_request
from schema.validation_job import ValidationJobSchema, ValidationJobSuccessSchema
from schema.error import ErrorResponseSchema, ErrorResponse422Schema
from schema.header import HeaderSchema
from logger import logger

validation_job_blp = Blueprint('validation', __name__)

@validation_job_blp.route('/validation/register')
class ValidationJobAPI(MethodView):

    @validation_job_blp.arguments(HeaderSchema, location="headers") 
    @validation_job_blp.arguments(ValidationJobSchema)
    @validation_job_blp.response(200, ValidationJobSuccessSchema)
    @validation_job_blp.response(400, ErrorResponseSchema)
    @validation_job_blp.response(403, ErrorResponseSchema)
    @validation_job_blp.response(422, ErrorResponse422Schema)
    def post(self, headers, data):
        """
        Registers a dataset for a given user.
        Accepts JSON body with 'dataset_id' and 'as_of_date'.
        Requires 'request_id' and 'X-Api-Token' in headers.
        """
        headers, code = validate_request_headers(headers)
        if code != 200:
            logger.warning(f"Header validation failed: {headers}")
            return jsonify({"errors": headers}), code
        
        response, code = process_validation_job_request(headers, data)
        if code != 200:
            logger.error(f"Processing validation job failed: {response}")
        else:
            logger.info(f"Validation job processed successfully for user {data.get('user_id', 'unknown')}")
        
        return response, code
