import logging
from flask import Flask, request, jsonify
from validator import validate_request_header, validate_validation_job
from service import process_validation_job_request

# --- 1. Configure Logging ---
# Set up a basic configuration for the logger.
# This will output logs to the console with a timestamp, log level, and message.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/validation/register/<user_id>', methods=['POST'])
def register_validation_request(user_id):
    """
    Registers a dataset for a given user.
    Accepts JSON body with 'dataset_id' and 'as_of_date'.
    Requires 'request_id' and 'X-Dummy-Token' in headers.
    """
    headers, code = validate_request_header(request)
    if code != 200:
        app.logger.warning(f"Header validation failed: {headers}")
        return jsonify({"error": headers}), code
    
    data, code = validate_validation_job(request)
    if code != 200:
        app.logger.warning(f"Body validation failed: {data}")
        return jsonify({"error": data}), code
    
    response, code = process_validation_job_request(headers, data, user_id)
    if code != 200:
        app.logger.error(f"Processing validation job failed: {response}")
    else:
        app.logger.info(f"Validation job processed successfully for user {user_id}")
    
    return response, code

if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts with common dev ports.
    app.run(debug=True, port=5001)
