from db import add_validation_request, fetch_records
from redis import push_validation_event
from flask import jsonify


def process_validation_job_request(headers, data):
    result = add_validation_request(headers, data)
    if result is None:
        message = "Failed to register validation request."
        return jsonify({"errors": message}), 500
    
    result = push_validation_event({
        "request_id": headers["request_id"],
        "dataset_id": data["dataset_id"],
        "as_of_date": data["as_of_date"],
        "table": data.get("table"),
        "table_group": data.get("table_group"),
    })

    if result is None:
        message = "Failed to enqueue validation event."
        return jsonify({"errors": message}), 500

    # --- Return Success Response ---
    response = {
        "status": "success",
        "message": "Validation request registered and event enqueued.",
        "user_id": data.get("user_id", "unknown"),
        "request_id_received": headers["request_id"],
        "data_received": data
    }

    return jsonify(response), 200


def fetch_data_cmp_request_master_records():
    table_name = "data_cmp_request_master"
    columns = [
        "ID",
        "GROUP_NAME",
        "SRC_ASOF",
        "SRC_DATASET_ID",
        "SRC_SCHEMA",
        "TGET_ASOF",
        "TGT_DATASET_ID",
        "TGT_SCHEMA",
        "TABLE_NAME",
        "REQUESTED_BY",
        "STATUS"
    ]

    records = fetch_records(table_name, columns)
    if records is False:
        response = {
            "status": "failed",
            "message": "Failed to retrieve the data from the database.",
            "data": []
        }
        return jsonify(response), 500
    
    response = {
        "status": "success",
        "message": "Validation request registered and event enqueued.",
        "data": records
    }

    return jsonify(response), 200 
