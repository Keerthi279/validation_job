from flask import Flask, request, jsonify
app = Flask(__name__)

DUMMY_AUTH_TOKEN = "ACCESS_TOKEN_FOR_API_AUTHENTICATION"

def validate_request_headers(headers):
    try:
        # Request Id validation logic
        pass
    except Exception as err:
        return err.messages, 400

    if headers["x_api_key"] != DUMMY_AUTH_TOKEN:
        return "Invalid API Key", 403

    return headers, 200


