import logging
from flask import Flask, request, jsonify
from api.validation_job import validation_job_blp
from flask_smorest import Api

# --- 1. Configure Logging ---
# Set up a basic configuration for the logger.
# This will output logs to the console with a timestamp, log level, and message.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
# Configure the Swagger UI
app.config["API_TITLE"] = "Validation Job API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(validation_job_blp)


if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts with common dev ports.
    app.run(debug=True, port=5001)
