from db import add_validation_request
from redis import push_validation_event
from flask import jsonify


def process_validation_job_request(headers, data, user_id):
    result = add_validation_request(headers, data)
    if result is None:
        message = "Failed to register validation request."
        return jsonify({"error": message}), 500
    
    result = push_validation_event({
        "request_id": headers["request_id"],
        "dataset_id": data["dataset_id"],
        "as_of_date": data["as_of_date"],
        "table": data.get("table"),
        "table_group": data.get("table_group"),
    })

    if result is None:
        message = "Failed to enqueue validation event."
        return jsonify({"error": message}), 500

    # --- Return Success Response ---
    response = {
        "status": "success",
        "message": "Validation request registered and event enqueued.",
        "user_id": user_id,
        "request_id_received": headers["request_id"],
        "data_received": data
    }

    return jsonify(response), 200
