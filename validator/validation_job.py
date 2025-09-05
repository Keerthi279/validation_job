from flask import Flask, request, jsonify
from marshmallow import ValidationError
from schema.validation_job import ValidationJobSchema
from logger import logger

validation_job_schema = ValidationJobSchema()

def validate_validation_job(request):
    logger.info("This function is not being used")
    return [], 200
